# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from os.path import join

from mycroft.util.lang import get_full_lang_code, get_primary_lang_code

from mycroft.util.lang.format_en import *
from mycroft.util.lang.format_pt import *
from mycroft.util.lang.format_it import *
from mycroft.util.lang.format_sv import *
from mycroft.util.lang.format_hu import *
from mycroft.util.lang.format_ar import *

from mycroft.util.lang.format_es import nice_number_es
from mycroft.util.lang.format_es import nice_time_es
from mycroft.util.lang.format_es import pronounce_number_es
from mycroft.util.lang.format_de import nice_number_de
from mycroft.util.lang.format_de import nice_time_de
from mycroft.util.lang.format_de import pronounce_number_de
from mycroft.util.lang.format_fr import nice_number_fr
from mycroft.util.lang.format_fr import nice_time_fr
from mycroft.util.lang.format_fr import pronounce_number_fr
from mycroft.util.lang.format_nl import nice_time_nl
from mycroft.util.lang.format_nl import pronounce_number_nl
from mycroft.util.lang.format_nl import nice_number_nl
from mycroft.util.lang.format_da import nice_number_da
from mycroft.util.lang.format_da import nice_time_da
from mycroft.util.lang.format_da import pronounce_number_da

from collections import namedtuple
from padatious.util import expand_parentheses
import json
import os
import datetime
import re

from ummalqura.hijri_date import HijriDate
from mycroft.util.time import now_local

def _translate_word(name, lang):
    """ Helper to get word tranlations

    Args:
        name (str): Word name. Returned as the default value if not translated.
        lang (str): Language code, e.g. "en-us"

    Returns:
        str: translated version of resource name
    """
    from mycroft.util import resolve_resource_file

    lang_code = get_full_lang_code(lang)

    filename = resolve_resource_file(join("text", lang_code, name+".word"))
    if filename:
        # open the file
        try:
            with open(filename, 'r', encoding='utf8') as f:
                for line in f:
                    word = line.strip()
                    if word.startswith("#"):
                        continue  # skip comment lines
                    return word
        except Exception:
            pass
    return name  # use resource name as the word


NUMBER_TUPLE = namedtuple(
    'number',
    ('x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000, ' +
     'x_in_x000, x0_in_x000, x_in_0x00'))


class DateTimeFormat:
    def __init__(self, config_path):
        self.lang_config = {}
        self.config_path = config_path

    def cache(self, lang):
        if lang not in self.lang_config:
            try:
                # Attempt to load the language-specific formatting data
                with open(self.config_path + '/' + lang + '/date_time.json',
                          'r') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())
            except FileNotFoundError:
                # Fallback to English formatting
                with open(self.config_path + '/en-us/date_time.json',
                          'r') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())

            for x in ['decade_format', 'hundreds_format', 'thousand_format',
                      'year_format']:
                i = 1
                while self.lang_config[lang][x].get(str(i)):
                    self.lang_config[lang][x][str(i)]['re'] = (
                        re.compile(self.lang_config[lang][x][str(i)]['match']
                                   ))
                    i = i + 1

    def _number_strings(self, number, lang):
        x = (self.lang_config[lang]['number'].get(str(number % 10)) or
             str(number % 10))
        xx = (self.lang_config[lang]['number'].get(str(number % 100)) or
              str(number % 100))
        x_in_x0 = self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10))) or str(int(number % 100 / 10))
        x0 = (self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10) * 10)) or
              str(int(number % 100 / 10) * 10))
        xxx = (self.lang_config[lang]['number'].get(str(number % 1000)) or
               str(number % 1000))
        x00 = (self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100) * 100)) or
               str(int(number % 1000 / 100) * 100))
        x_in_x00 = self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100))) or str(int(number % 1000 / 100))
        xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100) * 100)) or str(int(number % 10000 / 100) *
                                                 100)
        xx_in_xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100))) or str(int(number % 10000 / 100))
        x000 = (self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000) * 1000)) or
                str(int(number % 10000 / 1000) * 1000))
        x_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000))) or str(int(number % 10000 / 1000))
        x0_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000)*10)) or str(int(number % 10000 / 1000)*10)
        x_in_0x00 = self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100)) or str(int(number % 1000 / 100)))

        return NUMBER_TUPLE(
            x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000,
            x_in_x000, x0_in_x000, x_in_0x00)

    def _format_string(self, number, format_section, lang):
        s = self.lang_config[lang][format_section]['default']
        i = 1
        while self.lang_config[lang][format_section].get(str(i)):
            e = self.lang_config[lang][format_section][str(i)]
            if e['re'].match(str(number)):
                return e['format']
            i = i + 1
        return s

    def _decade_format(self, number, number_tuple, lang):
        s = self._format_string(number % 100, 'decade_format', lang)
        return s.format(x=number_tuple.x, xx=number_tuple.xx,
                        x0=number_tuple.x0, x_in_x0=number_tuple.x_in_x0,
                        number=str(number % 100))

    def _number_format_hundreds(self, number, number_tuple, lang,
                                formatted_decade):
        s = self._format_string(number % 1000, 'hundreds_format', lang)
        return s.format(xxx=number_tuple.xxx, x00=number_tuple.x00,
                        x_in_x00=number_tuple.x_in_x00,
                        formatted_decade=formatted_decade,
                        number=str(number % 1000))

    def _number_format_thousand(self, number, number_tuple, lang,
                                formatted_decade, formatted_hundreds):
        s = self._format_string(number % 10000, 'thousand_format', lang)
        return s.format(x_in_x00=number_tuple.x_in_x00,
                        xx00=number_tuple.xx00,
                        xx_in_xx00=number_tuple.xx_in_xx00,
                        x000=number_tuple.x000,
                        x_in_x000=number_tuple.x_in_x000,
                        x0_in_x000=number_tuple.x0_in_x000,
                        x_in_0x00=number_tuple.x_in_0x00,
                        formatted_decade=formatted_decade,
                        formatted_hundreds=formatted_hundreds,
                        number=str(number % 10000))

    """convert date to spoken Arabic format"""
    def date_format(self, dt, lang, now, DateType = 'G'):
        """initialize arrays of the Arabic days and months"""
        if DateType == 'H':
            ConvertedDT = HijriDate.get_hijri_date(dt.date()) 
            extractedDate = now.replace(microsecond=0)
            extractedDate = extractedDate.replace(year=int(ConvertedDT[0:4]), month=int(ConvertedDT[5:7]), day=int(ConvertedDT[8:]), tzinfo=extractedDate.tzinfo)
            dt = extractedDate

        days = {
    7: 'الأحد',
    1: 'الاثنين',
    2: 'الثلاثاء',
    3: 'الأربعاء',
    4: 'الخميس',
    5: 'الجمعة',
    6: 'السبت'
   }

        Gmonths = ['جانيوري', 'فبراير', 'مارس', 'أبريل', 'ماي', 'جون','جولاي', 'أوقست', 'سبتمبر', 'أكتوبر', 'نوفمبر','ديسمبر']
        Hmonths = ['محرم', 'صفر', 'ربيع الأول', 'ربيع الثاني', 'جماد الأول', 'جماد الثاني','رجب', 'شعبان', 'رمضان', 'شوال', 'ذي القعدة','ذي الحجة']
        HGYear = str(dt.year)[0:2]
        year = str(dt.year)[2:]
        if HGYear == '14':
            month = Hmonths[dt.month-1]
            BenningYear = 'ألف وأربع مائة و '
        elif HGYear == '20':
            month = Gmonths[dt.month-1]
            BenningYear = 'ألفين و '
        
        if now:
            """save tomorrow and yesteday dates"""
            tomorrow = now + datetime.timedelta(days=1)
            yesterday = now - datetime.timedelta(days=1)

            """now we check, if the given date is tomorrow then we retrieve غداً and so on"""
            if tomorrow.date() == dt.date():
                return 'غداً'
            elif now.date() == dt.date():
                return 'اليوم'
            elif yesterday.date() == dt.date():
                return 'أمس'
            if dt.year == now.year:
                return days[dt.weekday()+1] + " "+ pronounce_number(dt.day, lang) + " " +month
                
            """if the given date is not today or tomorrow or yesteday, then we need to generate a date using the bellow line of code"""
            return days[dt.weekday()+1] + " "+ pronounce_number(dt.day, lang) + " " +month + " "+ BenningYear + pronounce_number(int(year), lang)


    """Convert date and time into Arabic spoken format; it will concatenate the output of the two function (nice_time and date_format together)"""
    def date_time_format(self, dt, lang, now, use_24hour, use_ampm,DateType='G'):
        date_str = self.date_format(dt, lang, now,DateType)
        time_str = nice_time(dt, lang, use_24hour=use_24hour,
                             use_ampm=use_ampm)
        date_time = date_str + " "+ time_str
        return date_time

    def year_format(self, dt, lang, bc):
        number_tuple = self._number_strings(dt.year, lang)
        formatted_bc = (
            self.lang_config[lang]['year_format']['bc'] if bc else '')
        formatted_decade = self._decade_format(
            dt.year, number_tuple, lang)
        formatted_hundreds = self._number_format_hundreds(
            dt.year, number_tuple, lang, formatted_decade)
        formatted_thousand = self._number_format_thousand(
            dt.year, number_tuple, lang, formatted_decade, formatted_hundreds)

        s = self._format_string(dt.year, 'year_format', lang)

        return re.sub(' +', ' ',
                      s.format(
                          year=str(dt.year),
                          century=str(int(dt.year / 100)),
                          decade=str(dt.year % 100),
                          formatted_hundreds=formatted_hundreds,
                          formatted_decade=formatted_decade,
                          formatted_thousand=formatted_thousand,
                          bc=formatted_bc)).strip()


date_time_format = DateTimeFormat(
    os.path.dirname(os.path.abspath(__file__)) + '/../res/text')


def nice_number(number, lang=None, speech=True, denominators=None):
    """Format a float to human readable functions

    This function formats a float to human understandable functions. Like
    4.5 becomes 4 and a half for speech and 4 1/2 for text
    Args:
        number (int or float): the float to format
        lang (str): code for the language to use
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    # Convert to spoken representation in appropriate language
    lang_code = get_primary_lang_code(lang)
    if lang_code == "en":
        return nice_number_en(number, speech, denominators)
    elif lang_code == "es":
        return nice_number_es(number, speech, denominators)
    elif lang_code == "pt":
        return nice_number_pt(number, speech, denominators)
    elif lang_code == "it":
        return nice_number_it(number, speech, denominators)
    elif lang_code == "fr":
        return nice_number_fr(number, speech, denominators)
    elif lang_code == "sv":
        return nice_number_sv(number, speech, denominators)
    elif lang_code == "de":
        return nice_number_de(number, speech, denominators)
    elif lang_code == "hu":
        return nice_number_hu(number, speech, denominators)
    elif lang_code == "nl":
        return nice_number_nl(number, speech, denominators)
    elif lang_code == "da":
        return nice_number_da(number, speech, denominators)

    # Default to the raw number for unsupported languages,
    # hopefully the STT engine will pronounce understandably.
    return str(number)

"""convert time to spoken Arabic format"""
def nice_time(dt, lang=None, speech=True, use_24hour=False,
              use_ampm=True):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (str): code for the language to use
        speech (bool): format for speech (default/True) or display (False)
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    lang_code = get_primary_lang_code(lang)
    if lang_code == "en":
        return nice_time_en(dt, speech, use_24hour, use_ampm)
    elif lang_code == "es":
        return nice_time_es(dt, speech, use_24hour, use_ampm)
    elif lang_code == "it":
        return nice_time_it(dt, speech, use_24hour, use_ampm)
    elif lang_code == "fr":
        return nice_time_fr(dt, speech, use_24hour, use_ampm)
    elif lang_code == "de":
        return nice_time_de(dt, speech, use_24hour, use_ampm)
    elif lang_code == "hu":
        return nice_time_hu(dt, speech, use_24hour, use_ampm)
    elif lang_code == "nl":
        return nice_time_nl(dt, speech, use_24hour, use_ampm)
    elif lang_code == "da":
        return nice_time_da(dt, speech, use_24hour, use_ampm)
    elif lang_code == "pt":
        return nice_time_pt(dt, speech, use_24hour, use_ampm)
    elif lang_code == "ar":
        return nice_time_ar(dt, speech, use_24hour, use_ampm)

    # TODO: Other languages
    return str(dt)


def pronounce_number(number, lang=None, places=2, short_scale=True,
                     scientific=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5' would be 'five'

    Args:
        number: the number to pronounce
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool) : convert and pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    lang_code = get_primary_lang_code(lang)
    if lang_code == "en":
        return pronounce_number_en(number, places=places,
                                   short_scale=short_scale,
                                   scientific=scientific)
    elif lang_code == "it":
        return pronounce_number_it(number, places=places,
                                   short_scale=short_scale,
                                   scientific=scientific)
    elif lang_code == "es":
        return pronounce_number_es(number, places=places)
    elif lang_code == "fr":
        return pronounce_number_fr(number, places=places)
    elif lang_code == "de":
        return pronounce_number_de(number, places=places)
    elif lang_code == "hu":
        return pronounce_number_hu(number, places=places)
    elif lang_code == "nl":
        return pronounce_number_nl(number, places=places)
    elif lang_code == "da":
        return pronounce_number_da(number, places=places)
    elif lang_code == "pt":
        return pronounce_number_pt(number, places=places)
    elif lang_code == "ar":
        return pronounce_number_ar(number, places=places)

    # Default to just returning the numeric value
    return str(number)

"""convert date to spoken Arabic format"""
def nice_date(dt, lang=None, now=None, DateType = 'G'):
    """
    Format a datetime to a pronounceable date

    For example, generates 'tuesday, june the fifth, 2018'
    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (string): the language to use, use Mycroft default language if not
            provided
        now (datetime): Current date. If provided, the returned date for speech
            will be shortened accordingly: No year is returned if now is in the
            same year as td, no month is returned if now is in the same month
            as td. If now and td is the same day, 'today' is returned.
    Returns:
        (str): The formatted date string
    """
    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)

    return date_time_format.date_format(dt, full_code, now, DateType)

"""convert date and time to spoken Arabic format"""
def nice_date_time(dt, lang=None, now=None, use_24hour=False,
                   use_ampm=False, DateType='G'):
    """
        Format a datetime to a pronounceable date and time

        For example, generate 'الثلاثاء ثمانية أكتوبر الساعة السابعة مساءً'

        Args:
            dt (datetime): date to format (assumes already in local timezone)
            lang (string): the language to use, use Mycroft default language if
                not provided
            now (datetime): Current date. If provided, the returned date for
                speech will be shortened accordingly: No year is returned if
                now is in the same year as td, no month is returned if now is
                in the same month as td. If now and td is the same day, 'today'
                is returned.
            use_24hour (bool): output in 24-hour/military or 12-hour format
            use_ampm (bool): include the am/pm for 12-hour format
        Returns:
            (str): The formatted date time string
    """

    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)
    """it will be redirected to the function date_time_format"""
    return date_time_format.date_time_format(dt, full_code, now, use_24hour,
                                             use_ampm,DateType)


def nice_year(dt, lang=None, bc=False):
    """
        Format a datetime to a pronounceable year

        For example, generate 'nineteen-hundred and eighty-four' for year 1984

        Args:
            dt (datetime): date to format (assumes already in local timezone)
            lang (string): the language to use, use Mycroft default language if
            not provided
            bc (bool) pust B.C. after the year (python does not support dates
                B.C. in datetime)
        Returns:
            (str): The formatted year string
    """

    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)

    return date_time_format.year_format(dt, full_code, bc)

"""Convert duration to spoken Arabic words"""
def nice_duration(duration, lang=None, speech=True):
    """ Convert duration in seconds to a nice spoken timespan

    Examples:
       duration = 60  ->  "1:00" or "دقيقة"
       duration = 27  ->  "0:27" or "سبعة وعشرون ثانية"

    Args:
        duration: time, in seconds
        lang (str, optional): a BCP-47 language code, None for default
        speech (bool): format for speech (True) or display (False)
    Returns:
        str: timespan as a string
    """

    
    if type(duration) is datetime.timedelta:
        """convert the duration value to seconds"""
        duration = duration.total_seconds()

    # Do traditional rounding: 2.5->3, 3.5->4, plus this
    # helps in a few cases of where calculations generate
    # times like 2:59:59.9 instead of 3:00.
    duration += 0.5
    
    """after getting the duration in seconds, now it needs to be divided; sometimes the duration will be tranformed to one day and some hours and some minutes .. or it will be just hours or just 
    or just minutes and so on i.e. 60 is only 1 minute so it will be دقيقة or 3660 is an hour and minute so it will be ساعة و دقيقة"""
    days = int(duration // 86400)
    hours = int(duration // 3600 % 24)
    minutes = int(duration // 60 % 60)
    seconds = int(duration % 60)

    
    if speech:
        out = ""
        """if duration has days, then we need to see how many days it has been converted to i.e. 3 then get its prounouncable number i.e. ثلاثة"""
        if days > 0:
            out += pronounce_number(days, lang) + " "
            """if the duration is only one day them immidiatly just say يوم"""
            if days == 1:
                out = _translate_word("يوم", lang)
            #if the duration is only one day them immidiatly just say يومان
            elif days == 2:
                out = _translate_word("يومان", lang)
            elif days >2 and days <11:
                out += _translate_word("أيام", lang)
            else:
                out += _translate_word("يوم", lang)
        """if duration has hours, then we need to see how many hours it has to i.e. 3 then get its prounouncable number i.e. ثلاثة"""
        if hours > 0:
            if out:
                out += " "
            out += pronounce_number(hours, lang) + " "

            if hours == 1:
                out = _translate_word("ساعة", lang)
            elif hours == 2:
                out = _translate_word("ساعتان", lang)
            elif hours >2 and hours <11:
                out += _translate_word("ساعات", lang)
            else:
                out += _translate_word("ساعة", lang)
            

        if minutes > 0:
            if out:
                out += " "
            out += pronounce_number(minutes, lang) + " "

            if minutes == 1:
                out = _translate_word("دقيقة", lang)
            elif minutes == 2:
                out = _translate_word("دقيقتان", lang)
            elif minutes >2 and minutes <11:
                out+= _translate_word("دقائق", lang)
            else:
                out+= _translate_word("دقيقة", lang)
            

        if seconds > 0:
            if out:
                out += " "
            out += pronounce_number(seconds, lang) + " "

            if seconds == 1:
                out = _translate_word("ثانية", lang)
            elif seconds == 2:
                out = _translate_word("ثانيتين", lang)
            elif seconds >2 and seconds <11:
                out+= _translate_word("ثواني", lang)
            else:
                out+= _translate_word("ثانية", lang)
    #if we do not need mycroft to speak the duration to the user then just display it in it standard format      
    else:
        # M:SS, MM:SS, H:MM:SS, Dd H:MM:SS format
        out = ""
        if days > 0:
            out = str(days) + "d "
        if hours > 0 or days > 0:
            out += str(hours) + ":"
        if minutes < 10 and (hours > 0 or days > 0):
            out += "0"
        out += str(minutes)+":"
        if seconds < 10:
            out += "0"
        out += str(seconds)

    return out


def join_list(items, connector, sep=None, lang=None):
    """ Join a list into a phrase using the given connector word

    Examples:
        join_list([1,2,3], "and") ->  "1, 2 and 3"
        join_list([1,2,3], "and", ";") ->  "1; 2 and 3"

    Args:
        items(array): items to be joined
        connector(str): connecting word (resource name), like "and" or "or"
        sep(str, optional): separator character, default = ","
    Returns:
        str: the connected list phrase
    """

    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])

    if not sep:
        sep = ", "
    else:
        sep += " "
    return (sep.join(str(item) for item in items[:-1]) +
            " " + _translate_word(connector, lang) +
            " " + items[-1])


def expand_options(parentheses_line: str) -> list:
    """
    Convert 'test (a|b)' -> ['test a', 'test b']
    Args:
        parentheses_line: Input line to expand
    Returns:
        List of expanded possibilities
    """
    # 'a(this|that)b' -> [['a', 'this', 'b'], ['a', 'that', 'b']]
    options = expand_parentheses(re.split(r'([(|)])', parentheses_line))
    return [re.sub(r'\s+', ' ', ' '.join(i)).strip() for i in options]
