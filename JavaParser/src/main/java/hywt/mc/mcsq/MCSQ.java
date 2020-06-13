package hywt.mc.mcsq;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

public class MCSQ {
    public short version;
    public float multiplier;
    public List<Note> notes;

    public MCSQ(InputStream is) throws IOException {
        this.notes = new ArrayList<Note>();
        byte[] buffer = new byte[2];

        is.skip(4);
        is.read(buffer);
        this.version = Binary.bytes2Short(buffer);

        byte[] buffer4 = new byte[4];

        is.read(buffer4);
        multiplier = Binary.bytes2Float(buffer4);
        
        is.read(buffer4);
        int len = Binary.bytes2Int(buffer4);
        for (int i = 0; i < len; i++) {
        	is.read(buffer);
            short delta = Binary.bytes2Short(buffer);

            byte inst = (byte) is.read();

            byte pitch = (byte) is.read();
            notes.add(new Note(delta, inst, pitch));
        }
        is.close();
    }

    @Override
    public String toString() {
        return "MCSQ{" +
                "version=" + version +
                ", notes=" + notes +
                '}';
    }
}
