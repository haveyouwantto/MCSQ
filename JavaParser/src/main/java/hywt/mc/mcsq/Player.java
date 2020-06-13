package hywt.mc.mcsq;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.zip.GZIPInputStream;

import javax.sound.midi.MidiChannel;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.MidiUnavailableException;
import javax.sound.midi.Synthesizer;

public class Player {
	private int tick;
	private MidiChannel[] mChannels;
	private MCSQ mcsq;

	public void play(String file) throws FileNotFoundException, IOException, MidiUnavailableException, InterruptedException {
		Synthesizer midiSynth = MidiSystem.getSynthesizer();
		midiSynth.open();
		mChannels = midiSynth.getChannels();
		if (file.endsWith(".mcs")) {
			mcsq = new MCSQ(new FileInputStream(file));
		} else if (file.endsWith(".mcz")) {
			mcsq = new MCSQ(new GZIPInputStream(new FileInputStream(file)));
		} else {
			System.out.println("Invaild file");
			return;
		}
		System.out.println(String.format("MCSQ Version %04x", mcsq.version));
		System.out.println(String.format("Size: %08x", mcsq.notes.size()));
		this.changePrograms(mChannels);
		tick = 0;
		for (int i = 0; i < mcsq.notes.size(); i++) {
			Note n = mcsq.notes.get(i);
			switch (mcsq.version) {
			case 0:
				play(n);
				pause(n);
				break;
			case 1:
				pause(n);
				play(n);
				break;
			}

		}
	}

	public void pause(Note n) throws InterruptedException {
		if (n.delta > 0) {
			tick += n.delta;
			Thread.sleep(Math.round(n.delta * 50 * mcsq.multiplier));
			if (tick >= 8) {
				for (int j = 0; j < mChannels.length; j++)
					mChannels[j].allNotesOff();
				tick = 0;
			}
		}
	}

	private void play(Note n) {
		byte[] data = new byte[4];
		data[0] = (byte) (n.delta & 0xff);
		data[1] = (byte) ((n.delta >> 8) & 0xff);
		data[2] = n.inst;
		data[3] = n.pitch;
		System.out.println(String.format("%02x %02x %02x %02x  | ", data[0], data[1], data[2], data[3]) + n);
		switch (n.inst) {
		case 0:
			mChannels[0].noteOn(n.pitch, 100);
			break;
		case 1:
			mChannels[1].noteOn(n.pitch - 24, 100);
			break;
		case 2:
			mChannels[9].noteOn(36, 100);
			break;
		case 3:
			if (n.pitch > 66)
				mChannels[9].noteOn(42, 100);
			else
				mChannels[9].noteOn(38, 100);
			break;
		case 4:
			mChannels[9].noteOn(39, 100);
			break;
		case 5:
			mChannels[2].noteOn(n.pitch - 12, 100);
			break;
		case 6:
			mChannels[3].noteOn(n.pitch + 12, 100);
			break;
		case 7:
			mChannels[4].noteOn(n.pitch + 24, 100);
			break;
		case 8:
			mChannels[5].noteOn(n.pitch + 36, 100);
			break;
		case 9:
			mChannels[6].noteOn(n.pitch, 100);
			break;
		case 10:
			mChannels[7].noteOn(n.pitch, 100);
			break;
		case 11:
			mChannels[8].noteOn(n.pitch, 100);
			break;
		case 12:
			mChannels[10].noteOn(n.pitch, 100);
			break;
		case 13:
			mChannels[11].noteOn(n.pitch, 100);
			break;
		case 14:
			mChannels[12].noteOn(n.pitch, 100);
			break;
		case 15:
			mChannels[13].noteOn(n.pitch, 100);
			break;
		default:
			break;
		}
	}

	private void changePrograms(MidiChannel[] midiChannels) {
		midiChannels[0].programChange(0); // Harp
		midiChannels[1].programChange(32); // Bass
		midiChannels[2].programChange(24); // Guitar
		midiChannels[3].programChange(73); // Flute
		midiChannels[4].programChange(11); // Bell
		midiChannels[5].programChange(11); // Chime
		midiChannels[6].programChange(13); // Xylophone
		midiChannels[7].programChange(112); // Iron Xylophone
		midiChannels[8].programChange(112); // Cowbell
		midiChannels[10].programChange(29); // Didgeridoo
		midiChannels[11].programChange(80); // Bit
		midiChannels[12].programChange(105); // Banjo
		midiChannels[13].programChange(2); // Pling
	}
}
