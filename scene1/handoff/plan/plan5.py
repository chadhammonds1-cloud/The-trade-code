from PIL import Image, ImageDraw, ImageFont
import math
U=85; M=170; W,Dp=10,8
img=Image.new("RGB",(M*2+W*U+430, M*2+Dp*U+40),"white"); d=ImageDraw.Draw(img)
F=lambda s,b=False: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"%("-Bold" if b else ""),s)
f,fs,fb=F(17),F(14),F(19,True)
P=lambda x,y:(M+x*U,M+y*U)
def rect(x0,y0,x1,y1,fill,lab=None):
    d.rectangle([*P(x0,y0),*P(x1,y1)],fill=fill,outline="black",width=2)
    if lab: d.text(P((x0+x1)/2,(y0+y1)/2),lab,fill="black",font=fs,anchor="mm")
# walls: N and E solid (seen in locked images), W and S dashed (not shown yet)
d.line([P(0,0),P(W,0)],fill="black",width=6); d.line([P(W,0),P(W,Dp)],fill="black",width=6)
d.line([P(0,0),P(0,4.4)],fill="black",width=6)
for a,b in [((0,5.8),(0,Dp)),((0,Dp),(W,Dp))]:
    (x0,y0),(x1,y1)=a,b; n=40
    for i in range(0,n,2):
        d.line([P(x0+(x1-x0)*i/n,y0+(y1-y0)*i/n),P(x0+(x1-x0)*(i+1)/n,y0+(y1-y0)*(i+1)/n)],fill="#999",width=4)
d.text(P(0.75,6.9),"rest of west wall\nnot shown yet",font=fs,fill="#888",anchor="mm")
d.text(P(W/2,Dp+0.4),"SOUTH WALL — not shown in panorama or right view yet",font=fs,fill="#888",anchor="mm")
# north wall run, W->E, from panorama
rect(0,0,0.75,1.9,"#f2dcc0",None); d.text(P(0.375,0.95),"cab-\ninets",font=fs,fill="black",anchor="mm")
d.text(P(1.05,1.35),"lemons\nmixer",font=fs,fill="#664",anchor="lm")
rect(0,1.9,0.85,2.95,"#f5f5f5","FRIDGE")
d.text(P(1.05,2.45),"← doors face\n   the table",font=fs,fill="#555",anchor="lm")
d.ellipse([*P(0.1,3.05),*P(0.5,3.45)],fill="#7b5",outline="black")
d.line([P(0,3.6),P(0,4.2)],fill="#888",width=9); d.text(P(0.2,3.9),"calendar",font=fs,fill="black",anchor="lm")
d.line([P(0,4.4),P(0,5.8)],fill="white",width=10)
d.text(P(0.2,5.1),"HALLWAY\ndoorway",font=fs,fill="black",anchor="lm")
X0,Y0=P(-1.85,4.55); X1,Y1=P(-0.2,5.25)
d.rectangle([X0,Y0,X1,Y1],fill="#f6efe2",outline="#777")
[d.line([(X0+k*(X1-X0)/10,Y0),(X0+k*(X1-X0)/10,Y1)],fill="#a77",width=2) for k in range(1,10)]
d.line([(X1-10,(Y0+Y1)/2),(X0+14,(Y0+Y1)/2)],fill="#844",width=3)
d.polygon([(X0+6,(Y0+Y1)/2),(X0+20,(Y0+Y1)/2-8),(X0+20,(Y0+Y1)/2+8)],fill="#844")
d.text((X0+2,Y1+6),"STAIRS\nup toward west",font=fs,fill="#844",anchor="la")
rect(0.75,0,2.2,0.7,"#f2dcc0","cabinets")
rect(2.2,0,3.0,0.7,"#ffd27f","DRAWER")
d.text(P(1.6,0.95),"herb · boards · herbs",font=fs,fill="#664",anchor="mm")
rect(3.0,0,4.1,0.7,"#cfe3f5","SINK")
d.line([P(2.9,0),P(4.2,0)],fill="#2a6",width=9); d.text(P(3.55,-0.35),"WINDOW",font=fs,fill="#2a6",anchor="mm")
rect(4.1,0,7.0,0.7,"#f2dcc0","sanded cabinets")
for x in (5.7,6.3): d.rectangle([*P(x,0.75),*P(x+0.4,0.9)],fill="#d9a066",outline="black")
d.text(P(5.6,1.15),"leaning doors",font=fs,fill="#844",anchor="mm")
d.line([P(7.3,0),P(8.3,0)],fill="white",width=9); d.text(P(7.8,-0.35),"BACK DOOR",font=fs,anchor="mm",fill="black")
d.ellipse([*P(8.5,-0.08),*P(8.66,0.08)],fill="#c80"); d.text(P(8.6,0.35),"hook",font=fs,fill="#a60",anchor="mm")
d.text(P(9.15,-0.35),"picture",font=fs,fill="black",anchor="mm"); d.line([P(8.9,0),P(9.4,0)],fill="#888",width=8)
d.ellipse([*P(9.45,0.1),*P(9.9,0.55)],fill="#7b5",outline="black"); d.text(P(9.0,0.8),"plant",font=fs,fill="#363",anchor="mm")
# east wall N->S, from right view
rect(9.3,0.8,W,2.6,"#c98f55","PANTRY")
d.line([P(W,3.0),P(W,4.9)],fill="white",width=9); d.text((P(W,3.95)[0]+12,P(W,3.95)[1]),"DOORWAY to\nliving room",font=fs,fill="black",anchor="lm")
rect(9.1,5.1,W,6.6,"#f2dcc0","low cab.")
# table
cx,cy=P(4.0,4.2); r=1.05*U
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#d9a066",outline="black",width=2); d.text((cx,cy),"TABLE",font=f,anchor="mm")
for ang in (200,340,20,160):
    a=math.radians(ang); x=cx+1.45*U*math.cos(a); y=cy+1.45*U*math.sin(a)
    d.rectangle([x-18,y-18,x+18,y+18],outline="black",width=2,fill="#eee")
def who(x,y,c,t):
    X,Y=P(x,y); d.ellipse([X-17,Y-17,X+17,Y+17],fill=c,outline="black",width=2); d.text((X,Y),t,font=fb,fill="white",anchor="mm")
who(5.15,3.6,"#3a9a5b","V"); who(6.0,1.4,"#7a5230","D"); who(7.4,2.0,"#2f6fd1","T")
cams={1:(4.6,7.3,-90),2:(1.2,4.8,-25),3:(4.8,1.5,0),4:(8.2,2.8,-150),5:(4.0,5.4,-60),6:(7.3,3.9,-90),
      7:(6.8,4.8,-140),8:(1.9,6.3,-40),9:(4.3,2.1,-10),10:(8.6,3.2,-140),11:(7.8,2.5,-165),12:(3.3,5.6,-50),13:(8.7,4.4,-160),14:(6.4,3.4,-45)}
for n,(x,y,a) in cams.items():
    X,Y=P(x,y); r=math.radians(a); L=60
    col="#d22"
    for s in (-0.42,0.42): d.line([(X,Y),(X+L*math.cos(r+s),Y+L*math.sin(r+s))],fill=col,width=4)
    d.ellipse([X-14,Y-14,X+14,Y+14],fill=col); d.text((X,Y),str(n),font=fs,fill="white",anchor="mm")
d.text((M,16),"KITCHEN FLOOR PLAN v5 — panorama + right view + west wall view (locked)",font=fb,fill="black")
lx=M+W*U+170; ly=M
leg=[("PLATES",1),("Panorama / CENTER  looks N",0),("LEFT   looks NW: fridge (west",0),("   wall), corner cabinets, sink",0),("RIGHT  looks NE: back door,",0),("   hook, pantry, doorway",0),("WEST   looks W: hallway +",0),("   stairs, calendar, fridge",0),("",0),
     ("SHOT → PLATE",1),("1 CENTER    8 CENTER",0),("2 CENTER    9 RIGHT",0),("3 RIGHT    10 CENTER",0),("4 CENTER   11 LEFT",0),("5 CENTER   12 CENTER",0),("6 CENTER   13 WEST",0),("7 LEFT     14 RIGHT",0),("",0),
     ("V Vessa (seated)",0),("D Dad   T Tavique",0),("red = camera + view",0),("dashed = wall not",0),("   pictured yet",0)]
for i,(t,b) in enumerate(leg): d.text((lx,ly+i*27),t,font=fb if b else fs,fill="black")
img.save("floorplan_v5.png")
