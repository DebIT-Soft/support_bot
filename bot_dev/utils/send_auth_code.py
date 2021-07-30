from flask import Flask, session
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'support@debitsoft.ru'
app.config['MAIL_PASSWORD'] = 'Y4V_Vcen"?3gPjT*'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_email_thread(msg):
    with app.app_context():
        mail.send(msg)

def build_body(mail_to, username, code):
    with app.app_context():     
        # region Формирование сообщения
        up_part = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html style="width:100%;font-family:arial, \'helvetica neue\', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">\n<head> \n<meta charset="UTF-8"> \n<meta content="width=device-width, initial-scale=1" name="viewport"> \n<meta name="x-apple-disable-message-reformatting"> \n<meta http-equiv="X-UA-Compatible" content="IE=edge"> \n<meta content="telephone=no" name="format-detection"> \n<style type="text/css">\n#outlook a { padding:0;}\n.ExternalClass { width:100%;}\n.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height:100%;}\n.box-shadow { box-shadow:0 0 7px 1px #5050501f;}\n.es-button { mso-style-priority:100!important; text-decoration:none!important;}\na[x-apple-data-detectors] { color:inherit!important; text-decoration:none!important; font-size:inherit!important; font-family:inherit!important; font-weight:inherit!important; line-height:inherit!important;}\n.es-desk-hidden { display:none; float:left; overflow:hidden; width:0; max-height:0; line-height:0; mso-hide:all;}\n[data-ogsb] .es-button { border-width:0!important; padding:10px 25px 10px 25px!important;}\n[data-ogsb] .es-button.es-button-1 { padding:10px 25px!important;}\n'
        media_part = '@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1 { font-size:25px!important; text-align:center; line-height:120%!important } h2 { font-size:22px!important; text-align:center; line-height:120%!important } h3 { font-size:20px!important; text-align:center; line-height:120%!important } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:25px!important } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:22px!important } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important } .es-menu td a { font-size:16px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:13px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:16px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:11px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:14px!important; display:block!important; border-left-width:0px!important; border-right-width:0px!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }\n'
        part_a = '</style> \n</head> \n<body style="width:100%;font-family:arial, \'helvetica neue\', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"> \n<div class="es-wrapper-color" style="background-color:#F6F6F6"> \n<table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"> \n<tr style="border-collapse:collapse"> \n<td valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> \n<tr style="border-collapse:collapse"> \n<td class="es-info-area" align="center" style="padding:0;Margin:0"> \n<table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="center" valign="top" style="padding:0;Margin:0;width:560px"> \n<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> \n<tr style="border-collapse:collapse"> \n<td align="center" style="padding:0;Margin:0"> \n<table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#fff;width:600px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px"> \n<table class="es-left" cellspacing="0" cellpadding="0" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">\n' 
        part_b = '<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;width:268px"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p0l es-m-txt-c" align="left" style="padding:0;Margin:0;padding-top:15px;font-size:0"><img src="https://sun9-5.userapi.com/impg/S_UfmlcLDtvugPDaIuq_9cKO1LprODJ-z4YFmg/Ghgbr1pW0hg.jpg?size=250x40&quality=96&sign=4e123e99e818e21cc187c4717bb2227c&type=album" alt width="250" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table class="es-right" cellspacing="0" cellpadding="0" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;width:272px"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-txt-c" align="right" style="padding:0;Margin:0;padding-top:10px"><span class="es-button-border" style="border-style:solid;border-color:#0000FF;background:#0000FF;border-width:0px;display:inline-block;border-radius:0px;width:auto"><a href="https://t.me/DEBitSupport_bot/" class="es-button" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:18px;border-style:solid;border-color:#0000FF;border-width:10px 25px 10px 25px;display:inline-block;background:#0000FF;border-radius:0px;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-weight:bold;font-style:normal;line-height:22px;width:auto;text-align:center">Поддержка</a></span></td> \n</tr> \n</table></td> \n</tr> \n</table> </td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> \n<tr style="border-collapse:collapse"> \n<td align="center" style="padding:0;Margin:0;background-color:transparent" bgcolor="transparent"> \n<table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#090101;background-repeat:no-repeat;width:600px;background-image:url(https://sun9-1.userapi.com/impg/jlehzBMwEdb0Mm8UpHY0UXXa_TaC-H3_vYNPgw/0wL3oxonzL0.jpg?size=600x397&quality=96&sign=d2c4d9486f4a4e0ed1128f18d430981d&type=album);background-position:center top" background="https://sun9-1.userapi.com/impg/jlehzBMwEdb0Mm8UpHY0UXXa_TaC-H3_vYNPgw/0wL3oxonzL0.jpg?size=600x397&quality=96&sign=d2c4d9486f4a4e0ed1128f18d430981d&type=album"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-top:20px;background-position:center top"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;width:600px"> \n<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr class="es-mobile-hidden" style="border-collapse:collapse"> \n<td align="center" height="47" style="padding:0;Margin:0"></td> \n</tr> \n<tr style="border-collapse:collapse">\n'
        bef_uname_part = '<td align="left" class="es-m-txt-l" style="padding:0;Margin:0;padding-left:25px;padding-right:25px"><h2 style="Margin:0;line-height:45px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">Привет, '
        username = f'{username}!'
        aft_uname_part = '</h2><h2 style="Margin:0;line-height:45px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">Твой код потверждения:</h2></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td class="esdev-adapt-off" align="left" style="padding:0;Margin:0;padding-top:10px;padding-left:20px;padding-right:20px;background-position:center top"> \n<table cellpadding="0" cellspacing="0" class="esdev-mso-table" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:560px"> \n<tr style="border-collapse:collapse"> \n<td class="esdev-mso-td" valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p10r" align="center" style="padding:0;Margin:0;width:55px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px solid #FFFFFF;border-right:2px solid #FFFFFF;border-top:2px solid #FFFFFF;border-bottom:2px solid #FFFFFF;background-position:center top;border-radius:12px" role="presentation"> \n<tr style="border-collapse:collapse">\n' 
        bef_code1_part = '<td align="center" class="es-m-p10r es-m-p10l" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><h1 style="Margin:0;line-height:36px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">'
        code1 = f'{code[0]}'
        aft_code1_part = '</h1></td> \n</tr> \n</table></td> \n<td style="padding:0;Margin:0;width:15px"></td> \n</tr> \n</table></td> \n<td class="esdev-mso-td" valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p10r es-m-p10l" align="center" style="padding:0;Margin:0;width:55px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px solid #FFFFFF;border-right:2px solid #FFFFFF;border-top:2px solid #FFFFFF;border-bottom:2px solid #FFFFFF;background-position:center top;border-radius:12px" role="presentation"> \n<tr style="border-collapse:collapse"> \n'
        bef_code2_part = '<td align="center" class="es-m-p10r es-m-p10l" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><h1 style="Margin:0;line-height:36px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">'
        code2 = f'{code[1]}' 
        aft_code2_part = '</h1></td> \n</tr> \n</table></td> \n<td style="padding:0;Margin:0;width:15px"></td> \n</tr> \n</table></td> \n<td class="esdev-mso-td" valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p10r es-m-p10l" align="center" style="padding:0;Margin:0;width:55px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px solid #FFFFFF;border-right:2px solid #FFFFFF;border-top:2px solid #FFFFFF;border-bottom:2px solid #FFFFFF;background-position:center top;border-radius:12px" role="presentation"> \n<tr style="border-collapse:collapse"> \n'
        bef_code3_part = '<td align="center" class="es-m-p10r es-m-p10l" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><h1 style="Margin:0;line-height:36px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">'
        code3 = f'{code[2]}'
        aft_code3_part = '</h1></td> \n</tr> \n</table></td> \n<td style="padding:0;Margin:0;width:15px"></td> \n</tr> \n</table></td> \n<td class="esdev-mso-td" valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td align="center" class="es-m-p10r es-m-p10l" style="padding:0;Margin:0;width:55px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px solid #FFFFFF;border-right:2px solid #FFFFFF;border-top:2px solid #FFFFFF;border-bottom:2px solid #FFFFFF;background-position:center top;border-radius:12px" role="presentation"> \n<tr style="border-collapse:collapse"> \n'
        bef_code4_part = '<td align="center" class="es-m-p10r es-m-p10l" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><h1 style="Margin:0;line-height:36px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:30px;font-style:normal;font-weight:bold;color:#FFFFFF">'
        code4 = f'{code[3]}'
        aft_code4_part = '</h1></td> \n</tr> \n</table></td> \n<td style="padding:0;Margin:0;width:15px"></td> \n</tr> \n</table></td> \n<td class="esdev-mso-td" valign="top" style="padding:0;Margin:0"> \n<table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;width:280px"> \n<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="center" height="18" style="padding:0;Margin:0"></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-top:10px;background-position:center top"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="center" valign="top" style="padding:0;Margin:0;width:600px"> \n<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="left" class="es-m-txt-l" style="padding:0;Margin:0;padding-left:25px;padding-right:25px"><h5 style="Margin:0;line-height:150%;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#FFFFFF">Код действителен в течение 1 часа,</h5><h5 style="Margin:0;line-height:150%;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#FFFFFF">отправь его боту для подтвеждения</h5><h5 style="Margin:0;line-height:150%;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#FFFFFF">авторизации. Если ты не запрашивал его,</h5><h5 style="Margin:0;line-height:150%;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#FFFFFF">то воспользуйся кнопкой сверху.</h5></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td align="center" height="58" style="padding:0;Margin:0"></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> \n'
        part_c = '<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> \n<tr style="border-collapse:collapse"> \n<td align="center" style="padding:0;Margin:0"> \n<table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;background-position:center center"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p20b" align="center" valign="top" style="padding:0;Margin:0;width:270px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center top" role="presentation"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0"><h4 style="Margin:0;line-height:25px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#0000FF;font-size:21px">Мы в соц. сетях</h4></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-top:5px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#090101;font-size:14px">Подписывайся, чтобы быть в курсе всех новостей и обновлений.&nbsp;</p></td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;width:270px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center top" role="presentation"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0"><h4 style="Margin:0;line-height:25px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;color:#0000FF;font-size:21px">Связаться с нами</h4></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#090101;font-size:14px">Возникли проблемы? Обратись в поддержку. Автоматический прием заявок <a href="https://t.me/DEBitSupport_bot">здесь</a>.&nbsp;</p></td> \n</tr> \n</table></td> \n</tr> \n</table> </td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0;padding-bottom:10px;padding-left:20px;padding-right:20px;background-position:center top"> \n<table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:270px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center center" role="presentation"> \n<tr style="border-collapse:collapse"> \n'
        part_d = '<td align="left" bgcolor="transparent" style="padding:0;Margin:0;padding-top:10px;font-size:0;background-color:transparent"> \n<table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><img title="Instagram" src="https://llosnp.stripocdn.email/content/assets/img/social-icons/logo-black/instagram-logo-black.png" alt="Inst" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> \n<td align="center" valign="top" style="padding:0;Margin:0"><img title="Youtube" src="https://llosnp.stripocdn.email/content/assets/img/social-icons/logo-black/youtube-logo-black.png" alt="Yt" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right"> \n<tr style="border-collapse:collapse"> \n<td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:270px"> \n<table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center top" role="presentation"> \n<tr style="border-collapse:collapse"> \n<td style="padding:0;Margin:0"> \n<table class="es-table-not-adapt" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<td align="left" style="padding:0;Margin:0"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n</table></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td valign="top" align="center" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px;padding-right:5px;font-size:0"><img src="https://llosnp.stripocdn.email/content/guids/CABINET_d6b02eef486e424923e42d33952bbae0/images/34561561457385078.png" alt width="21" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> \n<td align="left" style="padding:0;Margin:0"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#090101;font-size:14px"><strong><a target="_blank" href="mailto:support@debitsoft.ru" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;color:#0000FF;font-size:14px">support@debitsoft.ru </a></strong></p></td> \n</tr> \n</table></td> \n</tr> \n<tr style="border-collapse:collapse"> \n<td valign="top" align="left" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px;padding-left:8px;padding-right:5px;font-size:0"><img src="https://llosnp.stripocdn.email/content/guids/CABINET_d6b02eef486e424923e42d33952bbae0/images/9911561457458673.png" alt width="21" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> \n<td align="left" style="padding:0;Margin:0"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#0000FF;font-size:14px"><strong>Краснодар</strong></p></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> </td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top"> \n<tr style="border-collapse:collapse"> \n<td align="center" style="padding:0;Margin:0"> \n<table bgcolor="#FFFFFF" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px;background-position:center top"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td align="center" valign="top" style="padding:0;Margin:0;width:560px"> \n<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center top" role="presentation"> \n'
        part_e = '</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> \n<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> \n<tr style="border-collapse:collapse"> \n<td align="center" style="padding:0;Margin:0"> \n<table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"> \n<tr style="border-collapse:collapse"> \n<td align="left" style="Margin:0;padding-left:20px;padding-right:20px;padding-top:30px;padding-bottom:30px;background-position:left top"> \n<table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n<tr style="border-collapse:collapse"> \n<td valign="top" align="center" style="padding:0;Margin:0;width:560px"> \n<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table></td> \n</tr> \n</table> \n</div>\n</body>\n</html>\n'
        message = up_part + media_part + part_a + part_b + bef_uname_part + username + aft_uname_part + bef_code1_part + code1 + aft_code1_part + bef_code2_part + code2 + aft_code2_part + bef_code3_part + code3 + aft_code3_part + bef_code4_part + code4 + aft_code4_part + part_c + part_d + part_e
        # endregion
        subject = f"Подтверждение авторизации"
        msg = Message(recipients=[mail_to], sender='DEBitSupport <support@debitsoft.ru>',
        subject=subject, html=message)
        thr = Thread(target=send_email_thread, args=[msg])
        thr.start()