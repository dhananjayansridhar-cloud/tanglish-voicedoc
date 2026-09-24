# Bench: `zm_obU5n8B0.wav`

- Audio 72.7 s, 9 phrases (VAD min silence 400 ms)
- ASR load 17.3 s, 2332 MiB allocated; translator load 4.3 s, total 2737 MiB
- Peak PyTorch GPU memory while running: 2770 MiB (excludes CUDA context, about 300-500 MiB)
- GPU: NVIDIA GeForce RTX 3050 6GB Laptop GPU

- Phrase latency after the pause (ASR native + translation): median 1.55 s, max 5.81 s

| end (s) | len (s) | ASR native | ASR mixed | English (from native) | English (from mixed) | asr s | mt s |
|---|---|---|---|---|---|---|---|
| 7.9 | 7.9 | நீ என் பைக் சாவி எங்கே வச்சேன்னு தெரியல தாங்க பைக் சாவி வேணா என்கிட்ட கேட்க வேண்டியது தானே நான்தான் உங்கள் பொண்டாட்டி | நீ என் bike சாவி எங்கே வச்சேன்னு தெரியல, இந்தாங்க bike சாவி வேணா என்கிட்ட கேட்க வேண்டியதுதானே? நான் தான் உங்க பொண்டாட்டி. | You don't know where the key to my bike comes from, you just have to ask me if I want the key to your bike, I'm your pony. | You don't know where my bike keys come from, do you need to ask me if I want the bike keys here? I'm your pony. | 3.26 | 2.55 |
| 17.2 | 4.4 | என் பொண்டாட்டி பைக் சாரி கேட்டால் இட்லி எடுத்துன்னு வந்துடுறாங்க | என் பொண்டாட்டி bike-ஐ கேட்டால் இட்லி எப்படி வந்தது? | If you ask me to ride my pony bike, I'll come get you an idli. | How did Idli come about if I asked for my Ponti bike? | 1.03 | 0.96 |
| 24.2 | 7.0 | நீ எந்த வேலையும் செய்ய வேணாம் எல்லாம் எங்கள் அண்ணி பார்த்துப்பாங்க உங்களுக்கு பொண்டாட்டி முக்கியமா அண்ணி முக்கியமா எனக்கு எங்கள் அண்ணி தான் முக்கியம் | நீ எந்த வேலையும் செய்ய வேணாம் எல்லாம் எங்கள் அண்ணி பார்த்துப்பாங்க. உங்களுக்கு பொண்டாட்டி முக்கியமா அண்ணி முக்கியமா? எனக்கு எங்கள் அண்ணி தான் முக்கியம். | Whatever work you want to do, our brother-in-law will take care of it. | Our brother-in-law will take care of whatever work you want to do. Is it important to you or is it important to me? | 1.88 | 1.66 |
| 27.6 | 2.9 | தெரியுமா | தெரியுமா? | Do you know | Do you know | 0.35 | 0.22 |
| 38.8 | 5.4 | பைக் தைக்கிறானா நீ | அடேய் சிரிக்காதீங்கண்ணே! | Are you riding a bike? | Don't laugh! | 0.47 | 0.35 |
| 53.1 | 7.2 | ஏன்டி கட்டிலுக்கு அடியில் என்னடி பண்றீங்க என்ன நடக்குதுங்க | ஏன்டி கட்டிலுக்கு அடியில் என்னடி பண்ணுறீங்க? என்ன நடக்குதுங்க? | Andy, what are you doing under the bed? | Andy, what are you doing under the bed? What's going on? | 0.96 | 0.58 |
| 57.7 | 3.0 | பாருமா தயவு செஞ்சு மூஞ்சி அப்படியே வைக்காதம்மா | பாருமா தயவு செஞ்சு மூஞ்சி அப்படியே வைக்காதம்மா | Please don't keep it like that. | Please don't keep it like that. | 1.06 | 0.48 |
| 59.9 | 1.2 | சரிங்க | என்ன செய்யணும்? | OK | What to do | 0.28 | 0.20 |
| 72.2 | 12.0 | உன் மேலே எவ்வளவு நம்பிக்கை வச்சிருக்கு கத்திரிக்கடையில் அப்படி பண்ணுறியடி சாவி எடுக்கிற இடமா அடியாது சாவி எடுக்கிற இடமா என்னென்ன பேசுகிறீங்க சாணாவுக்கு சாணா போடுறீங்களோ | உன் மேலே எவ்வளவு நம்பிக்கை வச்சிருக்கு கத்திரிக்கடையில் இப்படி பண்ணுறியடி சாவி எடுக்கிற இடமா அடியாது சாவி எடுக்கிற இடமா என்னென்ன பேசுகிறீங்க சாணாவுக்கு சாணா போடுறீங்களோ? | How much trust do you have in yourself? Do it at the grocery store, where you pick up the key, or where you take the key without hesitation, what are you talking about? | How much trust do you have in yourself? Do you do this at the grocery store, where you take the key or where you do not take the key, what are you talking about? | 2.94 | 1.73 |
