import java.lang.Math.*;
import java.util.*;

class HeightCoordinates {
	
	public double x,y,z,h;
	
	public static final double MAX_X = 30000.0;
	public static final double MAX_Y = 30000.0;
	public static final double MAX_H = 30000.0;
	
	
	HeightCoordinates(double xx, double yy, double hh)
	{
		x = xx;
		y = yy;
		h = hh;
	}

	HeightCoordinates(int xx, int yy, int hh)
	{
		x = xx;
		y = yy;
		h = hh;
	}

	HeightCoordinates add(HeightCoordinates other)
	{
		return primitive(this,other, 1.0);
	}

	HeightCoordinates sub(HeightCoordinates other)
	{
		return primitive(this, other, -1.0);
	}

	//See if this can be modified for the current object itself without creating the new object
	HeightCoordinates scale(double scale)
	{
		return new HeightCoordinates(scale*this.x, scale*this.y, scale*this.h);
	}

	double measure()
	{
		return Math.sqrt(this.x*this.x + this.y*this.y) + this.h;
	}

	boolean atOrigin()
	{
		return (this.x==0.0 && this.y==0.0);
	}

	boolean isValid()
	{
		return valid(this.x) && 
		valid(this.y) && 
		valid(this.h) && 
		Math.abs(this.x) <= MAX_X && 
		Math.abs(this.y) <= MAX_Y && 
		Math.abs(this.h) <= MAX_H;
	}

	double distance(HeightCoordinates other)
	{
		return this.sub(other).measure();
	}

	HeightCoordinates unity()
	{
		double m = this.measure();
		
		//Special Vivaldi Case, when u(0) = random unity vector
		if(m == 0.0)
		{
			return (new HeightCoordinates(Math.random()*1.0 ,Math.random()*1.0 ,Math.random()*1.0)).unity();
		}
		
		return this.scale(1/m);
	}

	void getCoordinates(double[] arr)
	{
		arr[0] = this.x;
		arr[1] = this.y;
	}

	void getCoordinates(ArrayList<Double> v)
	{
		v.add(this.x);
		v.add(this.y);
	}

	boolean equals(HeightCoordinates other)
	{
		if (other.x != this.x || other.y != this.y || other.h != this.h) {
			return false;
		}
				
		return true;
	}

	boolean valid(double f)
	{
		return (Double.isInfinite(f));
	}

	HeightCoordinates primitive(HeightCoordinates c1, HeightCoordinates c2, double scale)
	{
		return new HeightCoordinates(c1.x + c2.x * scale,
			c1.y + c2.y * scale,
			Math.abs(c1.h + c2.h)
		);
	}


	/*int main()
	{
		HeightCoordinates h1(0.0,0.0,0.0);
		HeightCoordinates h1u = h1.unity();
		std::cout<<h1<<std::endl;
		std::cout<<*h1u<<std::endl;
	}*/

}
