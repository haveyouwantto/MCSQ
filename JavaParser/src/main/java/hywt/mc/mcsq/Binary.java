package hywt.mc.mcsq;

public class Binary {

    public static short bytes2Short(byte[] bytes) {
        int int1 = bytes[0] & 0xff;
        int int2 = (bytes[1] & 0xff) << 8;

        return (short) (int1 | int2);
    }
    public static int bytes2Int(byte[] bytes) {
        int int1 = bytes[0] & 0xff;
        int int2 = (bytes[1] & 0xff) << 8;
        int int3 = (bytes[2] & 0xff) << 16;
        int int4 = (bytes[3] & 0xff) << 24;

        return int1 | int2 | int3 | int4;
    }
    public static float bytes2Float(byte[] b) {    
        int l;                                             
        l = b[0];                                  
        l &= 0xff;                                         
        l |= ((long) b[1] << 8);                   
        l &= 0xffff;                                       
        l |= ((long) b[2] << 16);                  
        l &= 0xffffff;                                     
        l |= ((long) b[3] << 24);                  
        return Float.intBitsToFloat(l);                    
    }  
}
