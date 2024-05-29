import django, pprint
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Odfelbot.settings'
django.setup()
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import Bot
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
from Odfelbot_API.models import *

TOKEN = config('TOKEN')
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def help(update, context):
    update.message.reply_text(
        """
        The following commands are available:

        /start - Welcome to ODFeLBOT
        /links - Gives all available whatsApp group links
        /announcement - List and Displays the most recent announcement
        /course Rep - Course Rep at all level and their contact info
        /about - Details of the BOT
        /help - List out all the available commands
        """
    )

def start(update, context):
    reply_keyboard = [
        ["/start ⌚"],
        ["/links 🔗"],
        ["/announcement 📄"],
        ["/courseReps 👥"],
        ["/about 🤖"],
        ["/help 🆘"],
    ]
    update.message.reply_text("Hello! 🙋‍♂️ Welcome to ODFeLBOT use the menu button to select available commands or use the listed options from the keyboard", reply_markup=ReplyKeyboardMarkup(reply_keyboard,))

def announcement(update, context):
    chat_id = update.message.chat.id
    announcement = Announcement.objects.all()[:3]

    notice_list = ""
    counter = 1
    for notice in announcement:
        notice_list += f"\n{counter}. {notice.title} \n\n{notice.desc}\n DATE: {notice.date_created}\n\n\n"
        counter += 1

    context.bot.send_message(chat_id=chat_id, text=notice_list, parse_mode='HTML')

def courseReps(update, context):
    keyboard = [[InlineKeyboardButton(f'{dept}', callback_data=f'{dept.pk}-CRdept')] for dept in Department.objects.all()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('<b>please select the Department you need course representatives information for?</b>', reply_markup=reply_markup, parse_mode='HTML')

def links(update, context):
    link_decision = ["session_links", "courses_links"] # 1-session, 2-courses
    keyboard = [[InlineKeyboardButton(str(pro), callback_data=f'{pro}-links')] for pro in link_decision]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Do you need session links or courses links?', reply_markup=reply_markup)

def about(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text='This bot provides information regarding ODFeL Kaduna Polytechnic 🏨, information such as social links 🔗, recent announcements by the center, course representatives 👥 information, and information about the BOT 🤖', parse_mode='HTML')

def button(update, context):
    chat_id = update.callback_query.message.chat.id
    query_data = update.callback_query.data.split('-')

    # COURSE REP
    if query_data[1] == 'CRdept':

        keyboard = [[InlineKeyboardButton(f'{level}', callback_data=f'{level.pk}-{query_data[0]}-CRLevel')] for level in Level.objects.all()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=f'please select the level you need course representatives information for?', reply_markup=reply_markup)

    try:

        if query_data[2] == 'CRLevel':

            qs = CourseRepresentative.objects.filter(level=query_data[0], department=query_data[1])

            if qs:

                qs_list = f'<b>{qs[0].level} {qs[0].department} course representative</b> ⬇️⬇️\n'
                for pro in qs:
                    qs_list += f'\nName: {pro.name}\nPhone: {pro.phone}\nDepartment: {pro.department}\nLevel: {pro.level}\n\n'

                context.bot.send_message(chat_id=chat_id, text=qs_list, parse_mode='HTML')
            else:
                context.bot.send_message(chat_id=chat_id, text=f'Unable to fetch course representatives record for {Department.objects.get(pk=query_data[0])} {Level.objects.get(pk=query_data[0])} 🥺')

    except: pass

    # LINKS
    if query_data[1] == 'links':

        if query_data[0] == "session_links":
            keyboard = [[InlineKeyboardButton(f'{sess}', callback_data=f'{sess.pk}-{query_data[0]}-SessLink')] for sess in Session.objects.all()]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=chat_id, text=f'please select the session you need links for?', reply_markup=reply_markup)

        if query_data[0] == "courses_links":
            # callback_data = dept-courses_link-DeptLink
            keyboard = [[InlineKeyboardButton(f'{dept}', callback_data=f'{dept.pk}-{query_data[0]}-DeptLink')] for dept in Department.objects.all()]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=chat_id, text=f'please select the department you need links for?',reply_markup=reply_markup)

    try:
        if query_data[2] == 'SessLink':
            qs = SessionLink.objects.filter(session=query_data[0])
            if qs:
                session_detail = f'<b>{qs[0].session} session link </b> ⬇️⬇️\n'
                for pro in qs:
                    session_detail += f'\nSession: {pro.session}\nLink: <a href="{pro.links}">{pro.links}</a>\n\n'
                context.bot.send_message(chat_id=chat_id, text=session_detail, parse_mode='HTML')
            else:
                context.bot.send_message(chat_id=chat_id, text=f'Unable to fetch {Session.objects.get(pk=query_data[0])} session link 🥺')

        if query_data[2] == 'DeptLink':
            # callback_data = level-dept-LevelLink
            keyboard = [[InlineKeyboardButton(f'{level}', callback_data=f'{level.pk}-{query_data[0]}-LevelLink')] for level in Level.objects.all()]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=chat_id, text=f'please select the level you need links for?',reply_markup=reply_markup)

        if query_data[2] == 'LevelLink':
            # callback_data = sem-level-dept-SemLink
            keyboard = [[InlineKeyboardButton(f'{sem}', callback_data=f'{sem.pk}-{query_data[0]}-{query_data[1]}-SemLink')] for sem in Semester.objects.all()]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=chat_id, text=f'please select the semester you need courses links for?',reply_markup=reply_markup)

        if query_data[3] == 'SemLink':
            qs = Links.objects.filter(semester=query_data[0], level=query_data[1], department=query_data[2])
            if qs:
                link_detail = f'<b>Below is all the links available for the {qs[0].semester} {qs[0].level} {qs[0].department} department</b> ⬇️⬇️\n'
                for pro in qs:
                    link_detail += f'\nCourse: {pro.course}\nLink: <a href="{pro.links}">{pro.links}</a>\n\n'
                context.bot.send_message(chat_id=chat_id, text=link_detail, parse_mode='HTML')
            else:
                context.bot.send_message(chat_id=chat_id, text=f'Unable to fetch {Semester.objects.get(pk=query_data[0])} {Level.objects.get(pk=query_data[1])} {Department.objects.get(pk=query_data[2])} department courses link 🥺')

    except: pass


# Register Commands
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('links', links))
dispatcher.add_handler(CommandHandler('announcement', announcement))
dispatcher.add_handler(CommandHandler('courseReps', courseReps))
dispatcher.add_handler(CommandHandler('about', about))

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

updater.start_polling()
updater.idle()