# -*- coding: utf-8 -*-
#
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
from collections import OrderedDict




_NUM_STRING_AR = {
    0: 'صفر',
    1: 'واحد',
    2: 'اثنين',
    3: 'ثلاثة',
    4: 'أربعة',
    5: 'خمسة',
    6: 'ستة',
    7: 'سبعة',
    8: 'ثمانية',
    9: 'تسعة',
    10: 'عشرة',
    11: 'أحد عشر',
    12: 'اثنا عشر',
    13: 'ثلاثة عشر',
    14: 'أربعة عشر',
    15: 'خمسة عشر',
    16: 'ستة عشر',
    17: 'سبعة عشر',
    18: 'ثمانية عشر',
    19: 'تسعة عشر',
    20: 'عشرون',
    30: 'ثلاثون',
    40: 'أربعون',
    50: 'خمسون',
    60: 'ستون',
    70: 'سبعون',
    80: 'ثمانون',
    90: 'تسعون'
}

_NUM_HOUR_AR = {
    0: 'الثانية عشر',
    1: 'الواحدة',
    2: 'الثانية',
    3: 'الثالثة',
    4: 'الرابعة',
    5: 'الخامسة',
    6: 'السادسة',
    7: 'السابعة',
    8: 'الثامنة',
    9: 'التاسعة',
    10: 'العاشرة',
    11: 'الحادية عشر',
    12: 'الثانية عشر'
 
}

WORDS_NUMBERS = {
    'صفر':0,
    'واحد':1,
    'اثنان':2,
    'اثنين':2,
    'ثلاثه':3,
    'اربعه':4,
    'خمسه':5,
    'سته':6,
    'سبعه':7,
    'ثمانيه':8,
    'تسعه':9,
    'عشره':10,



    'الحادي':1,
    'الثاني':2,
    'الثالث':3,
    'الرابع':4,
    'الخامس':5,
    'السادس':6,
    'السابع':7,
    'الثامن':8,
    'التاسع':9,
    'العاشر':10,
   


    'الواحده':1,
    'الثانيه':2,
    'الثالثه':3,
    'الرابعه':4,
    'الخامسه':5,
    'السادسه':6,
    'السابعه':7,
    'الثامنه':8,
    'التاسعه':9,
    'العاشره':10,



    'وحده':1,
    'ثنتين':2,
 

    'احد':1,
    'احدى':1,
    'اثني':2,
    'اثنا':2,
    'ثلاث':3,
    'اربع':4,
    'خمس':5,
    'ست':6,
    'سبع':7,
    'ثمان':8,
    'ثماني':8,
    'تسع':9,
    'عشر':10,


    'ثلاثا':3,
    'اربعا':4,
    'خمسا':5,
    'ستا':6,
    'سبعا':7,
    'تسعا':9,
    'عشرا':10,

    'طعش':10,

    'احدعش':11,
    'اثنعش':12,


    'عشرون':20,
    'ثلاثون':30,
    'اربعون':40,
    'خمسون':50,
    'ستون':60,
    'سبعون':70,
    'ثمانون':80,
    'تسعون':90,
    'مائه':100,
    'مئه':100,



    'عشرين':20,
    'ثلاثين':30,
    'اربعين':40,
    'خمسين':50,
    'ستين':60,
    'سبعين':70,
    'ثمانين':80,
    'تسعين':90,
    'ميه':100,


    'مئتان':200,
    'مئتين':200,
    'ميتين':200,
    'ثلاثمئه':300,
    'ثلاثميه':300,
    'ثلاثمائه':300,
    'اربعمئه':400,
    'اربعميه':400,
    'اربعمائه':400,
    'خمسمئه':500,
    'خمسميه':500,
    'خمسمائه':500,
    'ستمئه':600,
    'ستميه':600,
    'ستمائه':600,
    'سبعمئه':700,
    'سبعميه':700,
    'سبعمائه':700,
    'ثمانمئه':800,
    'ثمانميه':800,
    'ثمانمائه':800,
    'تسعمئه':900,
    'تسعميه':900,
    'تسعمائه':900,


    'الف':1000,
    'الفا':1000,

    'مليون':1000000,
    'مليار':1000000000,

    'الفان':2000,
    'الفين':2000,

    'مليونان':2000000,
    'مليونين':2000000,

    'ملياران':2000000000,
    'مليارين':2000000000,

   'الاف':1000,
    'ملايين':1000000,
    'مليارات':1000000000,
}

_FRACTION_STRING_AR = {
    2: 'half',
    3: 'third',
    4: 'forth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eigth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelveth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentyith'
}


_LONG_SCALE_AR = OrderedDict([
    (100, 'مئة'),
    (1000, 'آلاف'),
    (1000000, 'مليون'),
    (1e12, "بليون"),
    (1e18, 'ترليون'),
    (1e24, "quadrillion"),
    (1e30, "quintillion"),
    (1e36, "sextillion"),
    (1e42, "septillion"),
    (1e48, "octillion"),
    (1e54, "nonillion"),
    (1e60, "decillion"),
    (1e66, "undecillion"),
    (1e72, "duodecillion"),
    (1e78, "tredecillion"),
    (1e84, "quattuordecillion"),
    (1e90, "quinquadecillion"),
    (1e96, "sedecillion"),
    (1e102, "septendecillion"),
    (1e108, "octodecillion"),
    (1e114, "novendecillion"),
    (1e120, "vigintillion"),
    (1e306, "unquinquagintillion"),
    (1e312, "duoquinquagintillion"),
    (1e336, "sesquinquagintillion"),
    (1e366, "unsexagintillion")
])


_SHORT_SCALE_AR = OrderedDict([
    (100, 'مئة'),
    (1000, 'ألف'),
    (1000000, 'مليون'),
    (1e9, "بليون"),
    (1e12, 'ترليون'),
    (1e15, "quadrillion"),
    (1e18, "quintillion"),
    (1e21, "sextillion"),
    (1e24, "septillion"),
    (1e27, "octillion"),
    (1e30, "nonillion"),
    (1e33, "decillion"),
    (1e36, "undecillion"),
    (1e39, "duodecillion"),
    (1e42, "tredecillion"),
    (1e45, "quattuordecillion"),
    (1e48, "quinquadecillion"),
    (1e51, "sedecillion"),
    (1e54, "septendecillion"),
    (1e57, "octodecillion"),
    (1e60, "novendecillion"),
    (1e63, "vigintillion"),
    (1e66, "unvigintillion"),
    (1e69, "uuovigintillion"),
    (1e72, "tresvigintillion"),
    (1e75, "quattuorvigintillion"),
    (1e78, "quinquavigintillion"),
    (1e81, "qesvigintillion"),
    (1e84, "septemvigintillion"),
    (1e87, "octovigintillion"),
    (1e90, "novemvigintillion"),
    (1e93, "trigintillion"),
    (1e96, "untrigintillion"),
    (1e99, "duotrigintillion"),
    (1e102, "trestrigintillion"),
    (1e105, "quattuortrigintillion"),
    (1e108, "quinquatrigintillion"),
    (1e111, "sestrigintillion"),
    (1e114, "septentrigintillion"),
    (1e117, "octotrigintillion"),
    (1e120, "noventrigintillion"),
    (1e123, "quadragintillion"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "octogintillion"),
    (1e273, "nonagintillion"),
    (1e303, "centillion"),
    (1e306, "uncentillion"),
    (1e309, "duocentillion"),
    (1e312, "trescentillion"),
    (1e333, "decicentillion"),
    (1e336, "undecicentillion"),
    (1e363, "viginticentillion"),
    (1e366, "unviginticentillion"),
    (1e393, "trigintacentillion"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])


_ORDINAL_STRING_BASE_AR = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eighth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelfth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentieth',
    30: 'thirtieth',
    40: "fortieth",
    50: "fiftieth",
    60: "sixtieth",
    70: "seventieth",
    80: "eightieth",
    90: "ninetieth",
    10e3: "hundredth",
    1e3: "thousandth"
}


_SHORT_ORDINAL_STRING_AR = {
    1e6: "millionth",
    1e9: "billionth",
    1e12: "trillionth",
    1e15: "quadrillionth",
    1e18: "quintillionth",
    1e21: "sextillionth",
    1e24: "septillionth",
    1e27: "octillionth",
    1e30: "nonillionth",
    1e33: "decillionth"
    # TODO > 1e-33
}
_SHORT_ORDINAL_STRING_AR.update(_ORDINAL_STRING_BASE_AR)


_LONG_ORDINAL_STRING_AR = {
    1e6: "millionth",
    1e12: "billionth",
    1e18: "trillionth",
    1e24: "quadrillionth",
    1e30: "quintillionth",
    1e36: "sextillionth",
    1e42: "septillionth",
    1e48: "octillionth",
    1e54: "nonillionth",
    1e60: "decillionth"
    # TODO > 1e60
}
_LONG_ORDINAL_STRING_AR.update(_ORDINAL_STRING_BASE_AR)
