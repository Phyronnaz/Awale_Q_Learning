from learn_thread import LearnThread

LearnThread(epochs=100000, batch_size=512, memory_size=25000, gamma=0.9).run()
