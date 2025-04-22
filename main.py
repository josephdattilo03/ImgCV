import mido
from video_proc import list_macos_cameras, start_video_stream





def main(video_caputure_idx) :

    # note_on = mido.Message('note_on', note=70, velocity=64)
    # note_off = mido.Message('note_off', note=70, velocity=64)
    # note_on_2 = mido.Message('note_on', note=40, velocity=64)
    # note_off_2 = mido.Message('note_off', note=40, velocity=64)
    # outport = mido.open_output(mido.get_output_names()[0])    
    start_video_stream(video_caputure_idx)

    


if __name__ == "__main__":

    names = mido.get_output_names()
    dark_energy_index = 0 # replace with -1 later 
    # for i in range(len(names)):
    #     if names[i] == "USB MIDI Dark Energy   USB MIDI Dark Energy":
    #         dark_energy_index = i
    #         break
    # if dark_energy_index == -1:
    #     print("Dark Energy MIDI device not found")
    #     exit()
    for idx, device in enumerate(list_macos_cameras()):
        print(str(idx) + ": " + str(device))
    chosen_device = input("Select a device from the list above: ")
    main(int(chosen_device))