package hywt.mc.mcsq;

public class Note {
    public short delta;
    public byte inst;
    public byte pitch;

    public Note(short delta, byte inst, byte pitch) {
        this.delta = delta;
        this.inst = inst;
        this.pitch = pitch;
    }

    @Override
    public String toString() {
        return "Note{" +
                "delta=" + delta +
                ", inst=" + inst +
                ", pitch=" + pitch +
                '}';
    }
}
