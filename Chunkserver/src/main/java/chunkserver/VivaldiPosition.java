import java.lang.Math.*;
import java.util.*;

class VivaldiPosition {

	HeightCoordinates _coordinates;
	int _nbUpdates;
	double _error;	
	int CONVERGE_EVERY = 5;
	double CONVERGE_FACTOR = 50.0;
	double ERROR_MIN = 0.1;

	double cc = 0.25;
	double ce = 0.5;
	double initial_error = 10.0;

	VivaldiPosition(HeightCoordinates hc)
	{
		_coordinates = hc;
		_error = initial_error;
		_nbUpdates = 0;
	}

	public static VivaldiPosition create(double err)
	{
		VivaldiPosition vp = new VivaldiPosition(new HeightCoordinates(0,0,0));
		vp.setErrorEstimate( err );
		return vp;
	}

	public static VivaldiPosition create()
	{
		VivaldiPosition vp = new VivaldiPosition(new HeightCoordinates(0,0,0));
		vp.setErrorEstimate(0.0);
		return vp;
	}

	HeightCoordinates getCoordinates()
	{
		return this._coordinates;
	}

	void getLocation(double[] arr)
	{
		this._coordinates.getCoordinates(arr);
	}

	double getErrorEstimate()
	{
		return this._error;
	}

	void setErrorEstimate(double err)
	{
		_error = err;
	}

	boolean isValid()
	{
		return valid(_error) && this.getCoordinates().isValid();
	}

	double estimateRTT(HeightCoordinates data)
	{
		return this._coordinates.distance(data);
	}

	double estimateRTT(VivaldiPosition data)
	{
		HeightCoordinates coords = data.getCoordinates();
		
		if(coords.atOrigin() || this._coordinates.atOrigin())
		{
			return 1.0/0;//Infinity;//TODO:find a valid equivalent to NaN
		}
		
		return this._coordinates.distance(coords);
	}

	double[] toDoubleArray()
	{
		double[] arr = new double[4];
		arr[0] = this._coordinates.x;
		arr[1] = this._coordinates.y;
		arr[2] = this._coordinates.h;
		arr[3] = this._error;
		return arr;
	}

	VivaldiPosition fromDoubleArray(double[] data)
	{
		HeightCoordinates hc = new HeightCoordinates(data[0],data[1],data[2]);
		VivaldiPosition v = new VivaldiPosition(hc);
		v.setErrorEstimate(data[3]);
		
		return v;
	}

	boolean equals(VivaldiPosition other)
	{
		if (other._error != this._error) 
		{
			return false;
		}	
		
		if (!other._coordinates.equals(this._coordinates)) 
		{
			return false;
		}
		
		return true;
	}

	boolean valid(double f)
	{
		return (!Double.isInfinite(f));
	}


	boolean update(double rtt, HeightCoordinates cj, double ej)
	{
		if (!(valid(rtt) && cj.isValid() && valid(ej)) ) {
			System.out.println(this+" is invalid");
			return false;	// throw error may be
		}
		System.out.println(this+" is valid");
			
		double error = this._error;
		
		// Ensure we have valid data in input
		// (clock changes lead to crazy rtt values)
		if (rtt <= 0 || rtt > 5 * 60 * 1000) return false;
		if (error + ej == 0) return false;
		System.out.println(this+" is valid2");
		
		// Sample weight balances local and remote error. (1)
		double w = error / (ej + error);
		
		// Real error
		double re = rtt - this._coordinates.distance(cj);
		
		// Compute relative error of this sample. (2)
		double es = Math.abs(re) / rtt;
		
		// Update weighted moving average of local error. (3)
		double new_error = es * ce * w + error * (1 - ce * w);
		
		// Update local coordinates. (4)
		double delta = cc * w;
		double scale = delta * re;
		
		HeightCoordinates random_error = new HeightCoordinates(Math.random() / 10, Math.random() / 10, 0);
		
		HeightCoordinates new_coordinates = this._coordinates.add(this._coordinates.sub(cj.add(random_error)).unity().scale(scale));
		
		System.out.println("rand  error = "+random_error+" new_err = "+new_error+" "+new_coordinates);
		if (valid(new_error) && new_coordinates.isValid()) 
		{
			this._coordinates = new_coordinates;
			this._error = new_error > ERROR_MIN ? new_error : ERROR_MIN;
		} 
		else 
		{
			this._coordinates = new HeightCoordinates(0, 0, 0);
			this._error = initial_error;
		}
		
		if(!cj.atOrigin()) 
		{
			this._nbUpdates++;
		}
		if(this._nbUpdates > CONVERGE_EVERY) 
		{
			this._nbUpdates = 0;
			this.update(10,new HeightCoordinates(0,0,0),CONVERGE_FACTOR);
		}
		
		return true;
	}

	boolean update(double rtt, double[] cj, double ej)
	{
		return this.update(rtt, new HeightCoordinates(cj[0], cj[1], cj[2]), cj[3]);
	}

	boolean update(double rtt, VivaldiPosition cj, double ej)
	{
		return this.update(rtt, cj.getCoordinates(), cj.getErrorEstimate());
	}

	public String toString()
	{
		return "("+this._coordinates.x+", "+this._coordinates.y+")"; 
	}
	/*int main()
	{
		
	}*/

}
