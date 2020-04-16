p1 >> pluck([2, 2,2, 2, 2, 2, 2, 2, 2, 2, 4, 4],
    oct=5,
    amp=1,
    hpf=300,
    room=0.8,
    lpf=10000,
    slide=0,
    scale=Scale.major,
    dur=[0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 
        0.25, 0.25, 0.5, 0.5, 0.5])

p2 >> bass([2, 2, 2, 6],
    amp=0.4,
    lpf=300,
    oct=[5, 5, 5, 4])
        
p3 >> pluck(dur=1/2, 
    amp=sinvar([0,0.4], 2),
    room=0.8,
    hpf=1000,
    slide=0,
    pan=[-1, 1, -0.5, 0.5]).follow(p2) + (0, 7)
    
p4 >> glass(amp=1, room=0.8).follow(p2) + (0,5,7)


p5 >> play("x-o(-*)", amp=0.8,room = 0.4)


p6 >> play("s", amp=0.5, pan = 0.35, room = 0.4)
        
   
p1.stop()

p2.stop()

p3.stop()

p4.stop()

p5.stop()

p6.stop()


Clock.bpm = 140
