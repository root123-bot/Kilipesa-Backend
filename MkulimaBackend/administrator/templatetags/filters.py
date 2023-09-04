from django import template
import json
import datetime

register = template.Library()

@register.filter()
def computefarmsize(value):
    size_in_hectares = value / 10000
    # return {
    #     "meter": f"{value}m²",
    #     "hecta": "round(size_in_hectares, 3)hectras"
    # }
    return f"{round(value, 3)}m² / {round(size_in_hectares, 3)}hectras"


@register.filter()
def computeonlyhectras(value):
    print('daah')
    size_in_hectares = value / 10000
    # return only hecras..
    elems = str(size_in_hectares).split('.')

    if (len(elems[0]) > 3):
        return round(size_in_hectares, 1)
    return round(size_in_hectares, 3)

@register.filter()
def roundmetersquare(value):
    return round(value, 1)

@register.filter()
def formatphrase(phrase):
    return phrase[:50] + '...'

@register.filter()
def formatdatetime(dt):
    datetimestr = dt.strftime('%d/%m/%Y')
    return datetimestr


@register.filter()
def manipulateyieldamount(fertilizers):
    fertilizers = json.loads(fertilizers)
    fertilizers_vs_amount = []
    for fertilizer in fertilizers:
        fname = list(dict.keys(fertilizer))[0]
        fvalue = list(dict.values(fertilizer))[0]
        fertilizers_vs_amount.append(f'{fname} ... - ({fvalue}KG)...')

    return (', ').join(fertilizers_vs_amount)


@register.filter()
def manipulatefertilizerslist(fertilizers):
    fertilizers = json.loads(fertilizers)
    return (', ').join(fertilizers)


@register.filter()
def manipulatefertilizeramount(fertilizers):
    fertilizers = json.loads(fertilizers)
    fertilizers_vs_amount = []
    for fertilizer in fertilizers:
        fname = list(dict.keys(fertilizer))[0]
        fvalue = list(dict.values(fertilizer))[0]
        fertilizers_vs_amount.append(f'{fname} - ({fvalue}KG)')

    return (', ').join(fertilizers_vs_amount)


@register.filter()
def filtermonth(month):
    if int(month) == 1:
        return "Jan"

    elif int(month) == 2:
        return "Feb"

    elif int(month) == 3:
        return "Mar"

    elif int(month) == 4:
        return "Apr"

    elif int(month) == 5:
        return "May"

    elif int(month) == 6:
        return "Jun"

    elif int(month) == 7:
        return "Jul"

    elif int(month) == 8:
        return "Ago"

    elif int(month) == 9:
        return "Sept"

    elif int(month) == 10:
        return "Oct"

    elif int(month) == 11:
        return "Nov"

    elif int(month) == 12:
        return "Dec"
