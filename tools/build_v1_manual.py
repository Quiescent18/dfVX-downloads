"""Rebuild illustrated dfVX manual from existing public manual and verified GUI capture."""
from pathlib import Path
from io import BytesIO
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

base=Path("original_manual.pdf")
screen=Path("DfVx-window.png")
out=Path("dfVX_User_Manual_1.0.pdf")
pdfmetrics.registerFont(TTFont("DfBody","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DfBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
BLUE=HexColor("#009fba");INK=HexColor("#10242b");PALE=HexColor("#edf6f8")
GRAY=HexColor("#718491");BODY=HexColor("#293741")

def para(c,txt,x,top,w,size=9,leading=13,col=BODY):
    style=ParagraphStyle("body",fontName="DfBody",fontSize=size,leading=leading,textColor=col)
    item=Paragraph(txt,style)
    _,height=item.wrap(w,1000)
    item.drawOn(c,x,792-top-height)
    return top+height

def label(c,txt,x,y,size=10,col=BLUE):
    c.setFont("DfBold",size);c.setFillColor(col);c.drawString(x,792-y-size,txt)

def table(c,y,rows,widths=(93,184,225),heights=None):
    x=56; total=sum(widths)
    c.setFillColor(INK);c.rect(x,792-y-21,total,21,stroke=0,fill=1)
    for j,head in enumerate(["Selection","SYNC window","Edit windows"]):
        para(c,head,x+sum(widths[:j])+5,y+4,widths[j]-10,size=8,leading=11,col=HexColor("#ffffff"))
    y+=21
    for i,cols in enumerate(rows):
        h=heights[i] if heights else 54
        c.setFillColor(PALE if i%2==0 else HexColor("#ffffff"))
        c.rect(x,792-y-h,total,h,stroke=0,fill=1)
        for j,value in enumerate(cols):
            para(c,value,x+sum(widths[:j])+5,y+5,widths[j]-10,size=7.3,leading=10.3)
        y+=h
    return y

def new_page(number):
    mem=BytesIO();c=canvas.Canvas(mem,pagesize=(612,792))
    label(c,"dfVX / USER MANUAL",465,22,8)
    c.setFont("DfBody",7);c.setFillColor(GRAY)
    c.drawString(372,28,"dfVX  •  DOCUMENTATION EDITION 1.2   "+str(number))
    return c,mem

def finish(c,mem):
    c.save()
    return fitz.open(stream=mem.getvalue(),filetype="pdf")

im=Image.open(screen).convert("RGB")
w,h=im.size
crop=im.crop((int(w*.378),int(h*.155),int(w*.704),int(h*.805)))
crop.save("dfVX_manual_modulation_screenshot.png")

c,m=new_page(11)
label(c,"SECTION 07",56,52,8)
label(c,"Modulation",56,80,19,INK)
para(c,"Rotary speaker, independently selectable Phaser and Tremolo",56,117,495,9.5,13,GRAY)
aspect=crop.width/crop.height;targeth=343;targetw=targeth*aspect
c.drawImage("dfVX_manual_modulation_screenshot.png",(612-targetw)/2,792-143-targeth,targetw,targeth)
para(c,"Modulation panel: choose <b>ROTARY</b>, <b>PHASER</b>, <b>TREMOLO</b>, or both Phaser and Tremolo.",56,498,500,8.3,11.4,GRAY)
para(c,"Phaser and Tremolo are independent switches. Selecting either enables the Modulation stage. If it was bypassed with the older low mix, selection switches it to full Wet/Dry for an audible result. Both effects can run together.",56,523,499,8.6,12)
label(c,"ROTARY: SYNC / ROT1 EDIT / ROT2 EDIT",56,565,10)
# Narrower three-column table for Rotary on this page.
def rotary_table(c):
    y=587; widths=(67,214,221);x=56
    c.setFillColor(INK);c.rect(x,792-y-20,sum(widths),20,fill=1,stroke=0)
    for j,head in enumerate(["Page","Controls","Purpose"]):
        para(c,head,x+sum(widths[:j])+5,y+4,widths[j]-10,7,10,HexColor("#ffffff"))
    y+=20
    rows=[
      ["SYNC","FREE, 1/2, 1/4, 1/8, 1/16, 1/32; SLOW / FAST","Tempo division for rotor or free-running speeds."],
      ["ROT1 EDIT","H SLOW, H FAST, B SLOW, B FAST, DEPTH, WIDTH","Horn and bass speeds, depth and stereo width."],
      ["ROT2 EDIT","H ACCEL, B ACCEL, DOPPLER, CAB TONE, HORN MIX, BASS LVL","Rotor movement, tone, horn/bass blend."]]
    for i,row in enumerate(rows):
        height=34
        c.setFillColor(PALE if i%2==0 else HexColor("#ffffff"));c.rect(x,792-y-height,sum(widths),height,fill=1,stroke=0)
        for j,txt in enumerate(row):
            para(c,txt,x+sum(widths[:j])+5,y+4,widths[j]-10,7.3,10)
        y+=height
rotary_table(c)
para(c,"Changing a rotor rate while synced returns the upper division to FREE. DAW BPM controls rotor speed with a numbered division selected.",56,721,495,7.6,10.3)
page11=finish(c,m)

c,m=new_page(12)
label(c,"PHASER / TREMOLO: SELECT EITHER OR BOTH",56,52,10)
para(c,"With <b>Phaser</b> alone the upper SYNC grid controls Phaser sweep. With <b>Tremolo</b> alone it controls Tremolo volume pulses. Both can run independently.",56,79,497,9,13)
y=125
y=table(c,y,[
 ["PHASER only","Upper 1/2 to 1/32 follows DAW BPM; FREE uses PH RATE.","PHAS EDIT shows Phaser speed, stages, sweep, feedback, center and spread."],
 ["TREMOLO only","Upper 1/2 to 1/32 follows DAW BPM; FREE uses TR RATE.","TREM EDIT shows synced rate, depth, wave and MOD MIX. TR SYNC mirrors the upper grid."],
 ["BOTH selected","Upper grid controls Phaser. Tremolo uses TR DIV under TREM EDIT.","PHAS EDIT and TREM EDIT can use separate tempo divisions."]],heights=[55,55,58])
y+=24;label(c,"PHAS EDIT AND TREM EDIT",56,y,10);y+=22
para(c,"<b>PHAS EDIT:</b> PH RATE, STAGES (4/6/8), SWEEP, FEEDBACK, CENTER, PH SPREAD.",56,y,497,9,13);y+=30
para(c,"<b>TREM EDIT:</b> TR RATE, TR DEPTH, WAVE, TR SPREAD. Tremolo alone shows MOD MIX and TR SYNC. Both active show PH MIX and TR DIV.",56,y,497,9,13);y+=51
label(c,"RATE / TEMPO BEHAVIOR",56,y,10);y+=24
para(c,"While synchronized the edit-page RATE displays the <b>effective host-BPM-derived speed in Hz</b>. Adjusting the rate (not merely clicking) switches the applicable sync selector to <b>FREE</b>.",56,y,498,9,13);y+=66
para(c,"<b>Combined mode:</b> changing PH RATE sets the upper grid to FREE, while changing TR RATE sets TR DIV to FREE without changing Phaser sync. Non-rate adjustments do not cancel sync.",56,y,498,9,13);y+=67
c.setFillColor(PALE);c.roundRect(50,792-y-71,512,71,6,stroke=0,fill=1)
label(c,"SUGGESTED STARTING POINT",60,y+7,9)
para(c,"For Phaser start with 6 stages, Sweep 70-85%, Feedback 25-45%, Center 700-1000 Hz, PH MIX 50% and Modulation MIX 100%. Tremolo: start near 70% depth and try 1/8 sync.",60,y+24,486,8,11)
page12=finish(c,m)

result=fitz.open(base)
result.delete_page(11);result.insert_pdf(page12,start_at=11)
result.delete_page(10);result.insert_pdf(page11,start_at=10)
p=result[15]
p.draw_rect(fitz.Rect(65,110.4,554,130.4),color=None,fill=(.94,.97,.98),overlay=True)
p.insert_text((68,122.3),"TEMPO SYNC",fontsize=7.8,fontname="helv",color=(.16,.22,.27))
p.insert_text((145,122.3),"FREE, 1/2, 1/4, 1/8, 1/8D, 1/16",fontsize=7.4,fontname="helv",color=(.16,.22,.27))
p.insert_text((330,122.3),"Host-BPM musical repeat divisions.",fontsize=7.8,fontname="helv",color=(.16,.22,.27))
result.set_metadata({**result.metadata,"title":"dfVX 1.0 User Manual — Kisatchie Audio","subject":"Modulation controls, sync, phaser enhancements and half-note delay"})
result.save(out,garbage=4,deflate=True)
assert fitz.open(out).page_count==23
print("Generated",out,out.stat().st_size)
