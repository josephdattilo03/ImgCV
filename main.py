import mido
import time





def main():

    note_on = mido.Message('note_on', note=70, velocity=64)
    note_off = mido.Message('note_off', note=70, velocity=64)

    note_on_2 = mido.Message('note_on', note=40, velocity=64)
    note_off_2 = mido.Message('note_off', note=40, velocity=64)
    outport = mido.open_output(mido.get_output_names()[0])    
    while (True):
        outport.send(note_on)
        time.sleep(1)
        outport.send(note_off)
        outport.send(note_on_2)
        time.sleep(1)
        outport.send(note_off_2)

    


if __name__ == "__main__":

    names = mido.get_output_names()
    has_dark_energy = False
    for name in names:
        if name == "USB MIDI Dark Energy   USB MIDI Dark Energy":
            has_dark_energy = True
    if not has_dark_energy:
        print("Dark Energy MIDI device not found")
        exit()
    main()