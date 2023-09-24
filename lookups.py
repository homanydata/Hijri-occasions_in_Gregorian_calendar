class Links:
    MAIN_PAGE = "https://www.assirat.net/"
    
    def HIJRI_MONTH_PAGE(n):
        if 0 < n < 12:
            return f"https://www.assirat.net/calendar/gre_ann.php?id={n}"
        else:
            return "Error, month should be btw 1 and 12"

class Errors:
    Invalid_Month = "Error!! No number can be specified for an invalid month"
    Not_Full_Date_Format = "Not enough numbers found in the text"

def get_hijri_number(hijri_month):
    months_ordered = ['محرم','صفر','ربيع الاول','ربيع الثاني','جمادى الاول','جمادى الثاني','رجب','شعبان','رمضان','شوال','ذي القعدة','ذي الحجة']
    try:
        month_number = months_ordered.index(hijri_month) + 1
        return month_number
    except:
        return Errors.Invalid_Month