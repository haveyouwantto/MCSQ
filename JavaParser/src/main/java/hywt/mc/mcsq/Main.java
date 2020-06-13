package hywt.mc.mcsq;

import java.io.IOException;
import java.util.Arrays;

import javax.sound.midi.MidiDevice;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.MidiUnavailableException;
import javax.sound.midi.Synthesizer;

public class Main {
	public static void main(String[] args) {
		if (args.length < 1) {
			System.out.print("Missing input file");
			return;
		}
		Player p = new Player();
		try {
			p.play(args[0]);
		} catch (IOException | MidiUnavailableException | InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
