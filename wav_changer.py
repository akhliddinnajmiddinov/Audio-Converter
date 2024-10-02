from pydub import AudioSegment

fileName = "C://Users//Ahliddin&Asliddin//Desktop//Baza//1.2.wav"
music = AudioSegment.from_wav(fileName)
# print(dir(music[0]))
# print(music.max_possible_amplitude)

max_amplitude = music.max_possible_amplitude
for i in range(len(music)):
    # print(music[i].dBFS)
    music[i].dBFS /= max_amplitude
