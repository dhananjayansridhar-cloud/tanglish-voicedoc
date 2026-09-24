# Test bed report

Generated 2026-09-24 16:46 by `scripts/testbed.py`. ASR: Indic-Transcribe-flex, mixed script. Reference = YouTube Tamil auto-captions (another ASR system, not a human transcript), so CER is agreement, not accuracy.

GPU: NVIDIA GeForce RTX 3050 6GB Laptop GPU. Peak PyTorch VRAM with ASR + translator: `indictrans2-indic-en-dist-200M` 2767 MiB

| Clip | Note | Length | Phrases | Native CER vs captions | ASR median s | MT median s (indictrans2-indic-en-dist-200M) |
|---|---|---|---|---|---|---|
| [jOT8eHwlXHQ](https://www.youtube.com/shorts/jOT8eHwlXHQ) | TSEK tech talk, fast continuous Tanglish, single speaker | 138s | 14 | 12.1% | 1.13 | 0.64 |
| [upVmMFjZGQ0](https://www.youtube.com/shorts/upVmMFjZGQ0) | Kamal Haasan interview clip, film names and idioms | 47s | 4 | 11.8% | 1.32 | 0.89 |
| [zm_obU5n8B0](https://www.youtube.com/shorts/zm_obU5n8B0) | comedy, several speakers, background music and laughter | 73s | 9 | 346.8% | 0.39 | 0.32 |
| [wG6xp3AmNaM](https://www.youtube.com/shorts/wG6xp3AmNaM) | added by user 2026-09-24 | 97s | 23 | 19.7% | 0.41 | 0.26 |
| [8xgD-2qYdr0](https://www.youtube.com/shorts/8xgD-2qYdr0) | added by user 2026-09-24 | 60s | 6 | 31.3% | 0.95 | 0.54 |

## jOT8eHwlXHQ — How AI Is Revolutionizing Voice Typing | Learn from AI Applications - Tamil Series - Day 2

TSEK tech talk, fast continuous Tanglish, single speaker

| end s | ASR (mixed) | English (indictrans2-indic-en-dist-200M) |
|---|---|---|
| 5.5 | இன்னைக்கு day 1 of Learn From | Today is Day 1 of Learning From |
| 17.5 | AI applications day 1-இல் என்ன பார்க்க போகிறோம் அப்படின்னா என்ன மாதிரியான AI application-லாம் போயிட்டுருக்கு, especially voice related-ஆன AI application என்ன மாதிரி advancement போய்கிட்டுருக்கு அப்படிங்கிறத பற்றி பார்க்க போகிறோம். | What we are going to see in AI applications day 1 is what kind of AI application is going to go, especially voice-related AI application, what kind of advancement is going to happen. |
| 19.1 | முன்னிலாம் பார்த்தீங்கன்னா | Have you seen it before? |
| 31.1 | ஒரு speech to text transformation வந்து அவ்வளவு accurate-ஆக இருக்காது உங்களுக்கு நீங்கள் speech பண்ணுவீங்க அதை text-ஆக மாற்றும் அதோட accuracy diarrheasation-லாம் வந்து correct-ஆக இருக்காது எங்களுக்கு | A speech-to-text transformation will not be as accurate as if you were making a speech, converting it to text, and accuracy diarrheaation will not be correct for us. |
| 43.1 | பங்க்சுவேஷன் போடணும் இந்த மாதிரியான details-லாம் வந்து இருக்காது, but once OpenAI வந்து whisper models இதெல்லாம் வந்து release பண்ணதுக்கு அப்புறம் அதோட accuracy-ஐ பார்த்தீங்கன்னா | These kind of details may not come, but once OpenAI comes and whisper models come and release all these, then you have seen the accuracy. |
| 55.1 | 80% அந்த range-க்கு வந்து வர ஆரம்பிச்சிச்சு இப்போ பார்த்தீங்கன்னா 95% வரைக்கும் கூட வந்து accuracy வர ஆரம்பிச்சிடுச்சு அதாவது நீங்கள் English-இல் பேசினா கூட தமிழ் எது English எது? | 80 percent has started coming in that range and now you see that even up to 95 percent has started to come in accuracy that is even if you speak in English what is Tamil and what is English? |
| 67.1 | அப்படிங்கிற அளவுக்கு பிரிக்கிற அளவுக்கு multilingual accuracy வர ஆரம்பிச்சிருச்சு, for example, Deepgram, Cartesia இவங்கெல்லாம் வந்து அவ்வளவு accurate-ஆக வந்து predict பண்ணுறாங்க with AI help. | So much so that multilingual accuracy is starting to come in, for example, Deepgram, Cartesia are all coming in and predicting so accurately with AI help. |
| 79.4 | நம்மளோட speech-ஐ வந்து text-ஆக மாற்றுது இதனால் என்ன advancement என்ன மாதிரியான advancement real world applications-இல் அதாவது practical applications-இல் என்ன மாதிரியான advancement போயிட்டுருக்கு அப்படின்னு பார்த்தீங்கன்னா | Come with us and convert the speech into text so that you can see what kind of advancement is there in real world applications, that is, in practical applications. |
| 87.6 | Voice typing, for example, முந்தியெல்லாம் வந்து ஒரு form-ஐ fill பண்ணணும் இல்லை ஒரு ஒரு email அனுப்பணும் ஒரு | Voice typing, for example, doesn't always have to come in and fill out a form. |
| 98.8 | You know, data collect பண்ணணும் அப்படின்னா வந்து type பண்ணுறது அப்படிங்கிறது வந்து இருந்துச்சு. web forms அப்படிங்கிறது வந்து prominent-ஆக internet era-வில் இருந்துச்சு. இப்போ AI era-வில் | You know, data collection is coming and typing is happening. Web forms are coming and becoming prominent in the internet era. Now in the AI era. |
| 110.8 | இது கொஞ்சம் கொஞ்சமாக transform ஆகி structural input gathering அப்படிங்கிறது போய் ஒரு form-இல் வந்து நீங்கள் structured-ஆக input-ஐ வந்து gather பண்ணுறீங்க அப்படிங்கிறது போய் unstructured input-ஐ கூட | It gets transformed little bit and goes like a structural input gathering, you come in a form and you come and gather the structured input, you go and collect even the unstructured input. |
| 118.3 | வந்து gather பண்ணலாம் voice typing மூலமா அப்படிங்கிற மாதிரி application side-இல் இப்போ எல்லாரும் work பண்ண ஆரம்பிச்சிருக்காங்க. | Now everyone is starting to work on the application side, which can be done by voice typing. |
| 130.3 | இதோட evaluation இன்னும் faster-ஆக எல்லா applications-லேயும் இந்த voice related-ஆன adaption வந்து நடக்கும் அப்படிங்கிறத நான் predict பண்ணுறேன் இதுதான் இன்றைக்கி நாம் பார்க்குற விஷயம் | I predict that this voice-related adaptation will occur in all applications even faster, and this is what we are seeing today. |
| 137.8 | இதை பற்றி இன்னும் further-ஆக நீங்கள் learn பண்ணணும் அப்படின்னா என்னை subscribe பண்ணிக்கோங்க, follow பண்ணுங்கள். நான் உங்களுக்கு இன்னும் details சொல்கிறேன். | Subscribe and follow me if you want to learn more about this. I'll give you more details. |

## upVmMFjZGQ0 — Kamal's Inspiration for Hey Ram😲💥 | #heyram #kamalhaasan #shorts

Kamal Haasan interview clip, film names and idioms

| end s | ASR (mixed) | English (indictrans2-indic-en-dist-200M) |
|---|---|---|
| 12.0 | எனக்கு K.S. Gopalakrishnan-ஓட படம் பார்த்து இன்னைக்கும் அழுதுடுவேன் நான். technique-எல்லாம் அது காலம் போக போக மாற தான் செய்யும். அவர் black and white-இல் படம் எடுத்தார், நாங்கள் color-இல் எடுக்கிறோம். நான் அவர்கிட்ட சொன்னபோது என்ன? | I still cry when I watch K.S. Gopalakrishnan's Run. Technique - everything changes with time. He did the film in black and white, we do it in colour. What did I tell him? |
| 24.0 | கமல் நல்ல படத்தை பண்ணிட்டு அது எதுக்கு நான் சந்தோஷப்படுவேன்னு நினைக்கிறியா? நான் சந்தோஷப்பட மாட்டேன். Heram வேற படம், என்னதான் முடிவு வேற படம். நான் சொன்னேன், எனக்கு என்னதான் முடிவு தான் inspiration-ன்னு சொல்றேன். | Do you think I will be happy if Kamal makes a good film? I will not be happy. |
| 36.4 | அது எப்படி நீ சொல்லலாம்னு சண்டைக்கு வந்துட்டார், நீங்கள் சண்டைக்கு வர்றது உங்கள் பெருந்தன்மை, ஒத்துக்கிறது என் பெருந்தன்மை. நீங்கள் விட்டுருங்க, ஒருத்தனை கொல்லணும்னு கிளம்பிட்டு, அது அன்பே சிவத்துலேயும் இருக்கும், அது hero இல்லை அவன். | How can you say that he came to the fight, you come to the fight your greatness, I agree my greatness. You leave, you go out to kill someone, it will be love and redness, it is not a hero. |
| 46.5 | அவன் வில்லன் கொல்லணும்னு வந்துட்டு மனசு மாத்திக்கிறப்ப நீதான் நான் கடவுள்னு சொல்றது அந்த மாதிரி ஒரு படம் ஆனால் இந்த மாதிரி முன்னோடிகள் இருந்தே ஆகணும் | You are the one who says I am God when he comes to kill the villain and makes up his mind, it is a film like that but it is from pioneers like this. |

## zm_obU5n8B0 — 😂😂😂 #comedy  #funnyvideos #funny   #kpy #tamilcomedy  #memes#trending #viral #fun #funtimes

comedy, several speakers, background music and laughter

| end s | ASR (mixed) | English (indictrans2-indic-en-dist-200M) |
|---|---|---|
| 7.9 | நீ என் bike சாவி எங்கே வச்சேன்னு தெரியல, இந்தாங்க bike சாவி வேணா என்கிட்ட கேட்க வேண்டியதுதானே? நான் தான் உங்க பொண்டாட்டி. | You don't know where my bike keys come from, do you need to ask me if I want the bike keys here? I'm your pony. |
| 17.2 | என் பொண்டாட்டி bike-ஐ கேட்டால் இட்லி எப்படி வந்தது? | How did Idli come about if I asked for my Ponti bike? |
| 24.2 | நீ எந்த வேலையும் செய்ய வேணாம் எல்லாம் எங்கள் அண்ணி பார்த்துப்பாங்க. உங்களுக்கு பொண்டாட்டி முக்கியமா அண்ணி முக்கியமா? எனக்கு எங்கள் அண்ணி தான் முக்கியம். | Our brother-in-law will take care of whatever work you want to do. Is it important to you or is it important to me? |
| 27.6 | தெரியுமா? | Do you know |
| 38.8 | அடேய் சிரிக்காதீங்கண்ணே! | Don't laugh! |
| 53.1 | ஏன்டி கட்டிலுக்கு அடியில் என்னடி பண்ணுறீங்க? என்ன நடக்குதுங்க? | Andy, what are you doing under the bed? What's going on? |
| 57.7 | பாருமா தயவு செஞ்சு மூஞ்சி அப்படியே வைக்காதம்மா | Please don't keep it like that. |
| 59.9 | என்ன செய்யணும்? | What to do |
| 72.2 | உன் மேலே எவ்வளவு நம்பிக்கை வச்சிருக்கு கத்திரிக்கடையில் இப்படி பண்ணுறியடி சாவி எடுக்கிற இடமா அடியாது சாவி எடுக்கிற இடமா என்னென்ன பேசுகிறீங்க சாணாவுக்கு சாணா போடுறீங்களோ? | How much trust do you have in yourself? Do you do this at the grocery store, where you take the key or where you do not take the key, what are you talking about? |

## wG6xp3AmNaM — எனக்கும் பாலச்சந்தருக்கும் ஏற்பட்ட கருத்து மோதல்! | கவிஞர் வாலி சொன்ன Thug Life சம்பவம்!

added by user 2026-09-24

| end s | ASR (mixed) | English (indictrans2-indic-en-dist-200M) |
|---|---|---|
| 5.6 | அதை என்ன ஒரு சின்ன அதை விஷயமா ஒரு சம்மந்த ஒரு சந்தர்ப்பத்தில் ஒரு | It is a small matter of what it is and in a related case a |
| 7.8 | அது விஷயமா ஒரு சம்பவம் நடந்தது | There was an incident |
| 11.6 | அது தவிர்க்கப்பட வேண்டியது தான் இருந்தாலும் சுவாரஸ்யங்கிறதை சொல்கிறேன் | I'll tell you what's interesting, though it should be avoided. |
| 15.7 | ஏதோ ஒரு சின்ன misunderstanding அதுக்கு முந்தி எழுதின பாட்டில் எனக்கும் | I have a little misunderstanding about the bottle that was written before. |
| 17.2 | K. Balachandra | K. Balachandra |
| 18.8 | அவர்தான் director அதுக்கு | He is the director for it. |
| 23.9 | அந்த 1st பாட்டில் 2 பேரும் வந்து taly ஆகாமல் there was slight misunderstanding. | There was a slight misunderstanding when the 2 men in the 1st bottle arrived. |
| 27.2 | நான் தான் full picture எழுதுகிறேன் அதில் இந்த ஒரு பாட்டு தான் பாக்கி. | I am the one who is writing the full picture and this is the only song left. |
| 30.3 | So அவர் என்ன பண்ணிட்டார் இந்த situation-ஐ சொல்லிவிட்டு | So what did he do in this situation? |
| 33.7 | எழுதுங்க வாலி அப்படின்னாரே நான் எழுதினேன் | Write it down, that's what I wrote. |
| 37.4 | அந்த பாட்டு எழுதிட்டு இருக்கிற செயலை | The act in which the song is written |
| 39.5 | அவர் அந்த பாட்டு அவருக்கு பிடிச்சி போச்சு | He liked the song. |
| 42.0 | அப்புறம் பாட்டு முடிஞ்ச உடனே அவர் சொன்னார் | Then he said as soon as the song was over. |
| 47.3 | இந்த பாட்டு சும்மா எனக்கும் அவருக்கும் உள்ள மனஸ்தாபத்தை மனதில் வச்சுக்கிட்டு | This song is just keeping me and him in mind. |
| 50.9 | இந்த பாட்டு ஒரு தத்துவ பாட்டு | This song is a philosophy song. |
| 54.7 | இந்த 1 பாட்டை மட்டும் நான் கண்ணதாசனை வச்சு எழுதலாம்னு நினைச்சேன் | I thought I could write only this 1 song for Kannadasan. |
| 57.5 | இருந்தாலும் நீங்கள் நல்லா எழுதிவிட்டீங்க வேலை அப்படின்னார் | Anyway, you did a good job. |
| 60.6 | நான் கவிஞன் இல்லையா அதுவும் காவேரிக்கரை | Whether I am a poet or not, that is also Kaverikara. |
| 62.7 | சரண் நமக்கு கோபம் வந்தது | Charan got angry with us. |
| 66.2 | Dalit sir situation ரொம்ப அருமையான situation தான் | Dalit sir, the situation is very good. |
| 68.9 | இது இப்போ நான் என்ன உங்களுக்கு திருப்தின்னு தெரியல | I don't know what makes you happy now. |
| 78.1 | நானும் நினைச்சேன் இவ்வளோ அருமையான situation நீங்கள் சொல்கிறப்போ இந்த ஒரு பாட்டை மட்டும் குடும்ப கதையெல்லாம் direct பண்ணுற K.S. Gopalakrishnan direct பண்ணால் நல்லா இருக்குமே அப்படின்னு சொன்னேன் | I also thought that this is a wonderful situation and when you say this, I said that it would be better if K.S. Gopalakrishnan directs this one song to direct the whole family story. |
| 90.1 | Jan அதை அதில் எங்களுடைய அந்த கசப்பு உணர்ச்சி நகைச்சுவையெல்லாம் மறைஞ்சு போச்சு, so இந்த வெள்ளி விழான்ற போது அது நினைவில் வருது, but அதில் நல்ல பாடலா இருந்தது, but Bharatchandra நல்ல ரசிகர், அது எங்களுக்குள்ளே ஒரு சின்ன | It's a bittersweet comedy, so I remember it on this Friday, but it was a good song, but Bharatchandra is a good fan and it's a symbol among us. |

## 8xgD-2qYdr0 — Will you marry a doctor? ❤️😚 NON MEDICOS FUN answers 😂🔥 A2D reaction 💀😂 #shorts

added by user 2026-09-24

| end s | ASR (mixed) | English (indictrans2-indic-en-dist-200M) |
|---|---|---|
| 8.5 | Asking non-medicals, will they marry a doctor? இல்லைங்க, தட் வடக்கே கிளம்புறேன். | Asking non-medics, will they marry a doctor? |
| 17.4 | என்னது இது? | What's this? |
| 29.4 | பண்ணிப்பேன் Aditya Varma-வே ஒரு பையன் தான் எல்லாம். சீரியஸா? சீரியஸா? நீங்கள் நினைக்கிற Aditya Varma மாதிரிலாம் medical college-இல் இருக்க மாட்டாங்க. Definitely not, ஏன்னா இன்னைக்கு யாரும் friends இல்லை, doctor friends. | I'll make Aditya Verma a boy. Serious? Serious? You think you won't be in a medical college like Aditya Verma. Definitely not, because I don't have any friends, doctor friends. |
| 41.4 | அவங்க வந்து full-ஆக hospital-லயே இருப்பாங்கள்ல, அதுவும் இல்லாமல் ரொம்ப படிச்சிட்டா இருக்காங்க. ஏங்க, எனக்கு already கல்யாணமே ஆயிடுச்சுங்க. உங்களுக்கு கல்யாணம் ஆயிடுச்சா? சூடுங்க. Doctor தான் வேணும்னு இல்லை, அப்புறம் ஏதாவது நோய் வரும். | He's not going to be in the hospital full-time, but he's been through a lot without it. Wow, I'm already married. Are you getting married? Wow. You don't want a doctor, and then you're going to get sick. |
| 53.4 | நம்ம கேட்டுக்கலாம் அடிக்கடி நம்ம சும்மா Doctor, ஏதோ நல்லா இருக்கியே, super. அவங்க ரொம்ப படிச்சிக்கிட்டே இருப்பாங்க, அதை பற்றியே பேசுவாங்களோ எனக்கு ஒரு confusion இருக்குது. | We often ask if our only doctor, something is fine, is super. I have a confusion if he is very studious and talks about it. |
| 59.3 | எனக்குன்னே வருவீங்களாடா? என்கிட்ட சலசல் பண்றதுக்கே watch-ஆக போய் உங்களை பற்றி விளையாடா. | Won't you come with me? Don't go and play games with me just to make fun of me. |
