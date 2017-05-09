package chunkserver;

import java.util.*;

class Vivaldi {

	private static Vivaldi instance = null;
	
	private HashMap<String,VivaldiPosition> vMap;
	
	private Vivaldi()
	{
		vMap = new HashMap<String, VivaldiPosition>();
	}
	
	public static Vivaldi getInstance()
	{
		if(instance == null) instance = new Vivaldi();
		return instance;
	}
	
	public VivaldiPosition addNode(String ip)
	{
		if(vMap.containsKey(ip))
			return vMap.get(ip);
		
		VivaldiPosition v = VivaldiPosition.create(2);
		vMap.put(ip,v);
		return v;
	}
	
	public void removeNode(String ip)
	{
		if(vMap.containsKey(ip))
			vMap.remove(ip);
	}
	
	public void setDistance(String ip1, String ip2, double rtt)
	{
		if( !(vMap.containsKey(ip1) && vMap.containsKey(ip2)) )
			return;
		
		VivaldiPosition v1 = vMap.get(ip1);
		VivaldiPosition v2 = vMap.get(ip2);
		
		v1.update(rtt,v2,0.2);	
		//v2.update(rtt,v1,2.0);
		System.out.println(ip1+" to "+ip2+" = "+rtt);
		
	}
	
	public double getDistance(String ip1, String ip2)
	{
		if( !(vMap.containsKey(ip1) && vMap.containsKey(ip2)) )
			return 0.0;
		
		VivaldiPosition v1 = vMap.get(ip1);
		VivaldiPosition v2 = vMap.get(ip2);
		
		return v1.estimateRTT(v2);
	}
	
	public VivaldiPosition getNode(String ip)
	{
		return vMap.get(ip);
	}

	public static void main(String[] args)
	{
		Vivaldi v = Vivaldi.getInstance();
		v.addNode("x");
		v.addNode("y");
		v.addNode("z");
		v.addNode("w");
		
		v.setDistance("x","y",10);	
		
		v.setDistance("x","z",10);	
		v.setDistance("z","y",10);

			
		//v.setDistance("w","x",5);
		//v.setDistance("w","y",5);
		/*System.out.println(v.getNode("x"));
		System.out.println(v.getNode("y"));
		System.out.println(v.getNode("z"));
		System.out.println(v.getNode("w"));*/
		System.out.println(v.getDistance("x","z"));	
	}
}
