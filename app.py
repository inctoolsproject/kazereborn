import errno
import os
import sys
import tempfile

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi("nfyIfQMOsUJ0948KJkMbQAEdro5hsDXfW8QqSFHiVjcheRZP/g3yDojeRP+PXpElmAS/BLWvZdln2gFN8aPYI1HWTZaPEur1IVoHp+Qv/CAFPnHRd/Zs73HEQHEGJnJ3vz2XqJSPyuvROg5UfGHkAgdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("736dcf921090876bb87b6fc52cff9996")
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Terima kasih telah mengundang saya ke dalan group\nKetik !help untuk melihat event, team formation, dan fitur lainnya")) 
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
    
#=====[ LEAVE GROUP OR ROOM ]==========
     if text == "!me":
         if isinstance(event.source, SourceUser):
             profile = line_bot_api.get_profile(event.source.user_id)
             line_bot_api.reply_message(
                 event.reply_token, [
                     TextSendMessage(text="Nama: " + profile.display_name),
                     TextSendMessage(text="Status bio: " + profile.status_message)
                 ]
             )
         elif isinstance(event.source, SourceUser):
             profile = line_bot_api.get_profile(event.source.sender_id)
             line_bot_api.reply_message(
                 event.reply_token, [
                     TextSendMessage(text="Nama: " + profile.display_name),
                     TextSendMessage(text="Status bio: " + profile.status_message)
                 ]
             )
         else:
             line_bot_api.reply_message(
                 event.reply_token,
                 TextSendMessage(text="Bot can"t use profile in group chat"))

    if text == "!coss-bye":
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bye semuanya :D"))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bye semuanya :D"))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Command ini tidak bisa dipakai dalam private chat :("))

#=====[ TES MESSAGE ]=============
    elif text == "confirm":
        confirm_template = ConfirmTemplate(text="Bot nya bagus?", actions=[
            MessageTemplateAction(label="Yes", text="Yes!"),
            MessageTemplateAction(label="No", text="No!"),
        ])
        template_message = TemplateSendMessage(
            alt_text="Confirm alt text", template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)

#=====[ SEARCH ID LINE ]=============
    elif "!idline: " in event.message.text:
        skss = event.message.text.replace("/idline: ", "")
        sasa = "http://line.me/R/ti/p/~" + skss
        text_message = TextSendMessage(text=sasa)
        line_bot_api.reply_message(event.reply_token, text_message)
        return 0

    # elif "!contoh idline"

     elif "/apakah " in event.message.text:
         quo = ("Iya","Tidak","Gak tau","Bisa jadi","Mungkin iya","Mungkin tidak")
         jwb = random.choice(quo)
         text_message = TextSendMessage(text=jwb)
         line_bot_api.reply_message(event.reply_token, text_message)
         return 0

     elif (text == "999+") or (text == "999++"):
         message = TextSendMessage(text="ckk by")
         line_bot_api.reply_message(event.reply_token, message)

     elif (text == "Bot") or (text == "bot"):
         message = TextSendMessage(text="Siapa bot? ke bot an lu")
         line_bot_api.reply_message(event.reply_token, message)

     elif (text == "Tes") or (text == "tes") or (text == "Test") or (text == "test"):
         message = TextSendMessage(text="suk beybeh")
         line_bot_api.reply_message(event.reply_token, message)

     elif (text == "@") or (text == "Need") or (text == "need") or (text == "Need MoodBooster"):
         message = TextSendMessage(text="Apa manggil-manggil cogan")
         line_bot_api.reply_message(event.reply_token, message)

     elif text == ".":
         message = TextSendMessage(text="Titik titik amat so high lu")
         line_bot_api.reply_message(event.reply_token, message)

     elif (text == "Bah") or (text == "bah"):
         message = TextSendMessage(text="Beh")
         line_bot_api.reply_message(event.reply_token, message)

#=====[ TEMPLATE MESSAGE ]=============
     elif text == "/tools":
         buttons_template = TemplateSendMessage(
             alt_text="Tools message",
             template=ButtonsTemplate(
                 title="[ TOOLS MESSAGE ]",
                 text= "Tap the Button",
                 actions=[
                     MessageTemplateAction(
                         label="App Cloner",
                         text="/app clone"
                     ),
                     MessageTemplateAction(
                         label="Cek ID Line",
                         text="!contoh idline"
                     ),
                     MessageTemplateAction(
                         label="Your profile",
                         text="/me"
                     )
                 ]
             )
         )
        
         line_bot_api.reply_message(event.reply_token, buttons_template)
    elif (text == "!help") or (text == "help") or (text == "Help"):
        message = TemplateSendMessage(
            alt_text ="Help message",
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = "https://i.ibb.co/c8WzYwt/1551283598926.jpg",
                        title = "COSS Music Menu",
                        text = "Silahkan pilih\nTekan tombol dibawah ini",
                        actions = [
                            MessageTemplateAction(
                                label = "Random anime music",
                                text = "!random-anime-music"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://i.ibb.co/c8WzYwt/1551283598926.jpg",
                        title = "COSS Menu 2",
                        text = "Silahkan pilih, tekan tombol dibawah ini",
                        actions = [
                            MessageTemplateAction(
                                label = "Keluarkan bot",
                                text = "!COSS-Bye"
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)


    elif (text == "!About us") or (text == "!about us") or (text == "About us") or (text == "about us"):
        buttons_template = TemplateSendMessage(
            alt_text =" Help message",
            template = ButtonsTemplate(
                title = "LIST HELP",
                text = "silahkan pilih, tekan tombol dibawah ini",
                actions = [
                    MessageTemplateAction(
                        label = "comming soon",
                        text = "!commingsoon"
                    ),
                    MessageTemplateAction(
                        label = "Admin List",
                        text = "!adminlist"
                    ),
                    MessageTemplateAction(
                        label = "About COSS",
                        text = "!about coss "
                    ) 
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif "!commingsoon" in event.message.text:
        token = event.reply_token
        text_message = TextSendMessage(text = "Comming Soon...")
        line_bot_api.reply_message(token, text_message)
#=== [SEGAME TEAM] ===
    elif (text == "!about coss") or (text == "about coss") or (text == "About coss") or (text == "About Coss") or (text == "About COSS") or (text == "!About Coss"):
        token = event.reply_token
        buttons_template = TemplateSendMessage(
            alt_text = "ABOUT COSS",
            template = ButtonsTemplate(
                title = "ABOUT COSS",
                text = "Silahkam pilih game dibawah ini",
                actions = [
                    MessageTemplateAction(
                        label = "Mobile Legend",
                        text = "!mlbb team"
                    )
                ]
            )
        )
        line_bot_api.reply_message(token, buttons_template)

#=====[ CAROUSEL MESSAGE ]==========
    elif text == "/musik":
        buttons_template = TemplateSendMessage(
            alt_text="Enjoy whit music",
            template=ButtonsTemplate(
                title="[ GENDRE MUSIC ]",
                text= "Tap the Button",
                actions=[
                    MessageTemplateAction(
                        label="Music Indonesia",
                        text="/Mindo"
                    ),
                    MessageTemplateAction(
                        label="Music Barat",
                        text="/Mbarat"
                    ),
                    MessageTemplateAction(
                        label="Music Kpop",
                        text="/Mkpop"
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, buttons_template)
#=====[ CAROUSEL MESSAGE ]==========
    elif (text == "!adminlist") or (text == "Adminlist") or (text == "adminlist"):
        message = TemplateSendMessage(
            alt_text="Management COSS",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/zhFY7jg/linepy-1548249585-3.jpg",
                        title="SeGame Founder",
                        text="Pendiri SeGame E-sports",
                        actions=[
                            URITemplateAction(
                                label="YunSuh",
                                uri="https://line.me/ti/p/~YunSuh"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/nQkCwXQ/linepy-1547793990-2.jpg",
                        title="SeGame Moderator",
                        text="Pendiri bot official",
                        actions=[
                            URITemplateAction(
                                label="NvStar",
                                uri="https://line.me/ti/p/~kazereborn"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/qgR3DxQ/Screenshot-2.png",
                        title="SeGame Admin",
                        text="Admin SeGame E-sports",
                        actions=[
                            URITemplateAction(
                                label="Abang",
                                uri="https://line.me/ti/p/~rezafaesal22"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/W04LVGR/73316.jpg",
                        title="SeGame Admin",
                        text="Admin SeGame E-sports",
                        actions=[
                            URITemplateAction(
                                label="Penjual Kacang",
                                uri="https://line.me/ti/p/~dya_sudjono"
                            )
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.text == "!me":
        profile = line_bot_api.get_profile(event.source.user_id)
        buttons_template = TemplateSendMessage(
            alt_text="Profile Status",
            template=ButtonsTemplate(
                title="" + profile.display_name,
                text="Download photo profile klik dibawah ini",
                thumbnail_image_url="" + profile.picture_url,
                actions=[
                    URITemplateAction(
                        label="DOWNLOAD PHOTO",
                        uri="" + profile.picture_url,
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

#===========[RANDOM ANIME MUSIC]===========#
    if event.message.text == "!random-anime-music":
        request_url = requests.get("https://api.moe.team/animusic")
        data = request_url.text
        data = json.loads(data)
        music = data["data"]
        token = event.reply_token
        message_audio = AudioSendMessage(
            original_content_url = "{}".format(music["audio"]),
            duration = 240000
            ),
        buttons_template = TemplateSendMessage(
            alt_text = "Random anime music",
            template = ButtonsTemplate(
                title = "Judul : {}".format(music["title"]),
                text = "Klik dibawah ini untuk mendengarkan musik",
                thumbnail_image_url = "{}".format(music["image"]),
                actions = [
                    URITemplateAction(
                        label = "DENGARKAN MUSIK",
                        uri = "{}".format(music["audio"])
                        ),
                    MessageTemplateAction(
                        label = "Musik lainnya",
                        text = "!random-anime-music"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(token, buttons_template)
        return 0
#===============================

# [MUSIK COMMAND]

    elif "!musik " in event.message.text:
        query = event.message.text.replace("!musik ","")
        r = requests.get("http://ryns-api.herokuapp.com/joox?q={}".format(query))
        data = r.text
        data = json.loads(data)
        data2 = data["result"]
        jmlh = len(data2)
        datalagu = []
        if jmlh > 10:
            jmlh = 10
        else:
            pass
        for x in range(0,jmlh):
            item = CarouselColumn(
                thumbnail_image_url = "{}".format(str(data2[x]["img"])),
                title = "{}".format(str(data2[x]["title"])),
                text = "{}".format(str(data2[x]["artis"])),
                actions = [
                    URITemplateAction(
                        label = "{}".format(str(data2[x]["title"])),
                        uri = "{}".format(str(data2[x]["url"]))
                    )
                ]
            ),
            datalagu.append(item)
        buttons_template = TemplateSendMessage(
            alt_text = "SeGame Musik",
            template = CarouselTemplate(
                columns = [(str(datalagu))]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)  


    # elif "https://api.boteater.co/joox/single/"
#=====[ FLEX MESSAGE ]==========
     elif text == "need test":
         message = ImagemapSendMessage(
             base_url="https://i.ibb.co/c8WzYwt/1551283598926.jpg",
             alt_text="manyimak corom",
             base_size=BaseSize(height=1040, width=1040),
             actions=[
                 URIImagemapAction(
                     link_uri="https://line.me/ti/p/%40ajd1759p",
                     area=ImagemapArea(
                         x=0, y=0, width=520, height=1040
                     )
                 ),
                 MessageImagemapAction(
                     text="yudha ganteng",
                     area=ImagemapArea(
                         x=520, y=0, width=520, height=1040
                     )
                 )
             ]
         )
         line_bot_api.reply_message(event.reply_token, message)

#=====[ Sticker MESSAGE ]==========
     elif (text == "oksip") or (text == "Oksip"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002735/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "makasih") or (text == "Makasih"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/153453/IOS/sticker.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "nyimak") or (text == "Nyimak"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/13162615/IOS/sticker.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "ga") or (text == "gak") or (text == "gamau") or (text == "Gamau") or (text == "Ga") or (text == "Gak"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/8683557/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "good night") or (text == "Good night") or (text == "selamat malam") or (text == "Selamat malam"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/8683546/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "hai") or (text == "Hai") or (text == "halo") or (text == "Halo"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002738/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "sabar") or (text == "Sabar"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/22499899/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "wkwk") or (text == "Wkwk"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/27695296/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "hehe") or (text == "Hehe"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002763/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "siap") or (text == "Siap"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626520/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif text == "?":
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/34751035/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "please") or (text == "Please") or (text == "tolong") or (text == "Tolong"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626499/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "ok") or (text == "oke") or (text == "Ok") or (text == "Oke"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626500/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "hahaha") or (text == "Hahaha") or (text == "Haha")or (text == "haha"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/40381622/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
     elif (text == "sebel") or (text == "Sebel"):
         message = TemplateSendMessage(
             alt_text="NeedBot",
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52114135/IOS/sticker_animation@2x.png",
                         action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, message)
#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
