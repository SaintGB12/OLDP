#!/usr/bin/env python3
"""Fill oldp/locale/ar/LC_MESSAGES/django.po with Arabic translations.

Covers the public-facing UI (navigation, search, cases, laws, courts, contact,
errors). Admin / account / OAuth screens are left untranslated (English fallback).
Translations are a first draft: have a native speaker review legal terminology.

Usage:
    .venv/bin/python scripts/translate_ar.py
    cd oldp && ../.venv/bin/python ../manage.py compilemessages -l ar
"""
import polib

PO_PATH = "oldp/locale/ar/LC_MESSAGES/django.po"

T = {
    # Navigation / generic
    "Cases": "القضايا",
    "Case": "قضية",
    "Laws": "القوانين",
    "Law": "قانون",
    "Courts": "المحاكم",
    "Court": "المحكمة",
    "References": "المراجع",
    "Home": "الرئيسية",
    "Search": "بحث",
    "Contact": "اتصل بنا",
    "About": "حول",
    "Blog": "المدونة",
    "Imprint": "إشعار قانوني",
    "Privacy": "الخصوصية",
    "Terms": "الشروط",
    "Documentation": "التوثيق",
    "Examples": "أمثلة",
    "Contribute": "ساهم",
    "Statistics": "إحصائيات",
    "Overview": "نظرة عامة",
    "Login": "تسجيل الدخول",
    "Sign In": "تسجيل الدخول",
    "Sign Out": "تسجيل الخروج",
    "Sign Up": "إنشاء حساب",
    "Signup": "إنشاء حساب",
    "Account": "الحساب",
    "Dashboard": "لوحة التحكم",
    "English": "الإنجليزية",
    "German": "الألمانية",
    "Arabic": "العربية",
    # Case page
    "Court chamber": "الغرفة",
    "Decision type": "نوع القرار",
    "Source": "المصدر",
    "btn_go_to_source": "الانتقال إلى المصدر",
    "Found at": "موجود في",
    "Download": "تحميل",
    "File number": "رقم الملف",
    "Published on": "نُشر في",
    "Publication date": "تاريخ النشر",
    "Last modified date": "تاريخ آخر تعديل",
    "Jurisdiction": "الاختصاص",
    "Level of Appeal": "درجة التقاضي",
    "State": "الدولة / الجهة",
    "Country": "البلد",
    "Short-URL": "رابط مختصر",
    "btn_show_full_text": "عرض النص الكامل",
    "btn_show_all": "عرض الكل",
    "Cited by": "مستشهد به في",
    "Open citing-cases search": "فتح البحث عن القضايا المستشهِدة",
    "Show all %(cases_count)s cases ...": "عرض كل القضايا (%(cases_count)s) ...",
    "No other cases cite this decision yet.": "لا توجد قضايا أخرى تستشهد بهذا القرار بعد.",
    "Referenced by": "مُشار إليه في",
    "No cases cite this section yet.": "لا توجد قضايا تستشهد بهذه المادة بعد.",
    "This document does not contain any references.": "لا تحتوي هذه الوثيقة على أي مراجع.",
    "This content does not contain any references.": "لا يحتوي هذا المحتوى على أي مراجع.",
    "Cases citing": "القضايا التي تستشهد بـ",
    "Cases citing case": "القضايا التي تستشهد بالقضية",
    "(unknown)": "(غير معروف)",
    "Unknown topic": "موضوع غير معروف",
    "Has reference to": "يحيل إلى",
    "Court title": "اسم المحكمة",
    "ECLI code": "رمز ECLI",
    # Laws
    "View all laws": "عرض كل القوانين",
    "More Laws": "المزيد من القوانين",
    "Law book": "مدونة القوانين",
    "Changelog": "سجل التغييرات",
    "Revisions": "المراجعات",
    "selected": "محدد",
    "Warning:": "تنبيه:",
    "law_outdated_warning": "قد يكون نص هذا القانون قديماً لأن المحتوى غير محدَّث باستمرار. يرجى التحقق من المصادر الرسمية.",
    "This law is deprecated.": "هذا القانون ملغى.",
    "not assigned": "غير محدد",
    # Search
    "No results": "لا توجد نتائج",
    "Your search <strong>%(query)s</strong> did not match any documents.": "لم يطابق بحثك <strong>%(query)s</strong> أي وثيقة.",
    "Suggestions": "اقتراحات",
    "Make sure that all words are spelled correctly.": "تأكد من أن جميع الكلمات مكتوبة بشكل صحيح.",
    "Try different keywords.": "جرّب كلمات مفتاحية مختلفة.",
    "Try more general keywords.": "جرّب كلمات مفتاحية أكثر عمومية.",
    "Try fewer keywords.": "جرّب عدداً أقل من الكلمات المفتاحية.",
    "No filter available.": "لا توجد مرشحات متاحة.",
    "Sort by": "ترتيب حسب",
    "Relevance": "الأهمية",
    "Date (newest first)": "التاريخ (الأحدث أولاً)",
    "Most cited first": "الأكثر استشهاداً أولاً",
    "Document type": "نوع الوثيقة",
    "Search tips": "نصائح للبحث",
    "Remove filter": "إزالة المرشح",
    "Filters": "المرشحات",
    "Apply filters": "تطبيق المرشحات",
    "Apply": "تطبيق",
    "Reset": "إعادة تعيين",
    "All": "الكل",
    "After": "بعد",
    "Before": "قبل",
    "Last day": "اليوم الأخير",
    "Last week": "الأسبوع الأخير",
    "Last month": "الشهر الأخير",
    "Last three month": "الأشهر الثلاثة الأخيرة",
    "Last year": "السنة الأخيرة",
    "Last 5 years": "السنوات الخمس الأخيرة",
    "All time": "كل الفترات",
    "Date": "التاريخ",
    "Count": "العدد",
    "Total": "المجموع",
    "cases": "قضايا",
    "Name": "الاسم",
    "descending": "تنازلي",
    "Name (Z-A)": "الاسم (ي-أ)",
    "Search is currently unavailable. Please try again later.": "البحث غير متاح حالياً. يرجى المحاولة لاحقاً.",
    "Sorry, we could not find any results.": "عذراً، لم نعثر على أي نتائج.",
    "%(count)s documents sorted by <b>date</b>.": "%(count)s وثيقة مرتبة حسب <b>التاريخ</b>.",
    "%(count)s documents sorted by <b>most cited</b>.": "%(count)s وثيقة مرتبة حسب <b>الأكثر استشهاداً</b>.",
    "%(count)s documents sorted by <b>relevance</b>.": "%(count)s وثيقة مرتبة حسب <b>الأهمية</b>.",
    "%(count)s citing cases, sorted by <b>date</b>.": "%(count)s قضية مستشهِدة، مرتبة حسب <b>التاريخ</b>.",
    "%(count)s citing cases, sorted by <b>relevance</b>.": "%(count)s قضية مستشهِدة، مرتبة حسب <b>الأهمية</b>.",
    "%(start)s-%(end)s of %(count)s items": "%(start)s-%(end)s من %(count)s عنصر",
    "%(start)s-%(end)s of > %(max_count)s items": "%(start)s-%(end)s من أكثر من %(max_count)s عنصر",
    "search_query_placeholder": "قانون، كلمة مفتاحية، ...",
    "search_example_queries": "أمثلة على البحث",
    # Homepage
    "homepage_banner_title": "وصول مجاني إلى المعلومات القانونية",
    "homepage_banner_text1": "نوفر وصولاً مجانياً ومفتوحاً إلى الوثائق القانونية للعموم وللأنظمة الآلية.",
    "homepage_banner_text2": "تُضاف الوثائق الحديثة بانتظام إلى قاعدة بياناتنا.",
    "Latest Cases": "أحدث القضايا",
    "View all cases": "عرض كل القضايا",
    "Free Access to Legal Information": "وصول مجاني إلى المعلومات القانونية",
    "Free Access to Legal Data": "وصول مجاني إلى البيانات القانونية",
    "Open Data": "بيانات مفتوحة",
    "Legal Research": "البحث القانوني",
    "Increase Transparency": "تعزيز الشفافية",
    "Join the team!": "انضم إلى الفريق!",
    "Read more about the project.": "اقرأ المزيد عن المشروع.",
    "Our Blog": "مدونتنا",
    "Show more posts": "عرض المزيد من المقالات",
    "Getting Started with the API": "البدء مع واجهة البرمجة",
    "We have different endpoints for cases, laws, courts and more.": "نوفر نقاط وصول مختلفة للقضايا والقوانين والمحاكم وغيرها.",
    "Try it out!": "جرّبها!",
    # Statistics
    "Case Statistics": "إحصائيات القضايا",
    "Cases by Country": "القضايا حسب البلد",
    "Cases by State": "القضايا حسب الجهة",
    "Cases by Court": "القضايا حسب المحكمة",
    "Cases by Source": "القضايا حسب المصدر",
    "By Country": "حسب البلد",
    "By State": "حسب الجهة",
    "By Court": "حسب المحكمة",
    "By Source": "حسب المصدر",
    "Group by": "تجميع حسب",
    "Month": "الشهر",
    "Year": "السنة",
    "Day": "اليوم",
    "yearly": "سنوي",
    "monthly": "شهري",
    "daily": "يومي",
    "Select a state": "اختر جهة",
    "View": "عرض",
    "Loading statistics...": "جارٍ تحميل الإحصائيات...",
    "Error loading statistics": "خطأ في تحميل الإحصائيات",
    "Explore by Dimension": "الاستكشاف حسب البُعد",
    "Download (JSON)": "تحميل (JSON)",
    # Contact / report
    "Full name": "الاسم الكامل",
    "Email address": "البريد الإلكتروني",
    "Message": "الرسالة",
    "Write here your message!": "اكتب رسالتك هنا!",
    "You have to write something!": "يجب أن تكتب شيئاً!",
    "Submit": "إرسال",
    "Report content": "الإبلاغ عن محتوى",
    "Source URL": "رابط المصدر",
    "Type of infringement": "نوع الانتهاك",
    "Copyright Infringement": "انتهاك حقوق النشر",
    "Additional information": "معلومات إضافية",
    "Please provide more details on your complaint.": "يرجى تقديم مزيد من التفاصيل حول شكواك.",
    "Invalid input.": "مدخل غير صالح.",
    "Other": "أخرى",
    # Errors
    "Error": "خطأ",
    "Not found": "غير موجود",
    "The requested content does not exist.": "المحتوى المطلوب غير موجود.",
    "Go back": "رجوع",
    "Back to homepage": "العودة إلى الصفحة الرئيسية",
    "Bad request": "طلب غير صالح",
    "You sent an invalid request.": "لقد أرسلت طلباً غير صالح.",
    "Permission denied": "تم رفض الإذن",
    "You do not have sufficient rights for this action.": "ليست لديك الصلاحيات الكافية لهذا الإجراء.",
    # Misc
    "Status": "الحالة",
    "Save": "حفظ",
    "Cancel": "إلغاء",
    "Confirm": "تأكيد",
    "Remove": "إزالة",
    "Email": "البريد الإلكتروني",
    "Username": "اسم المستخدم",
    "API": "واجهة البرمجة (API)",
    "PDF": "PDF",
    "ECLI": "ECLI",
}


def main():
    po = polib.pofile(PO_PATH)
    done = 0
    for entry in po:
        if entry.msgid_plural:
            continue
        tr = T.get(entry.msgid)
        if tr:
            entry.msgstr = tr
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            done += 1
    po.metadata["Language"] = "ar"
    po.metadata["Last-Translator"] = "Draft"
    po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
    po.save()
    print("translated %d / %d entries" % (done, len(po)))


if __name__ == "__main__":
    main()
