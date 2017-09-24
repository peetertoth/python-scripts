#!/usr/bin/env python
# -*- coding: ISO-8859-2 -*-

import sys

class SubjectInstance():
    def __init__(self, title, course, courseType, teacher, day, time, place):
        self.title = title
        self.course = course
        self.courseType = courseType
        self.teacher = teacher
        self.day = day
        self.time = time
        self.place = place
        # TODO: amennyiben később előfordulna hosszabb, rövidebb órák
        self.begin = self.time[0:2]
        self.length = 2
        self.value = 0
        # ODOT

    def print_html_form(self):
        #rowspan=\"" + str(self.length) + "\" 
        retval = ("<td class=\"" + self.courseType + "\" id=\"kr" + str(self.value) + "\"onclick=\"highlight(this)\">" +
                  self.title + "<br>" + self.course + "<br>" + self.teacher + "<br>" + self.day + " - " + self.time + "<br>" + self.place + "</td>")
        #print(retval)
        return retval

def print_blank_td():
    return "<td class=\"emp\" onclick=\"highlight(this)\"> &empty; </td>"

def day_to_int(day):
    day = day.lower()
    return { "h" : 0, "k" : 1, "sze" : 2, "cs" : 3, "p" : 4}.get(day, -1)

def begin_to_int(begin):
    return { "08" : 0, "09" : 1, "10" : 1,
             "11" : 2, "12" : 2, "13" : 3,
             "14" : 4, "15" : 4, "16" : 5,
             "18" : 6}.get(begin, -1)

#-------------------------------------------------#
# Fájl megnyitása és tartalom rendezett betöltése #
# Az elkészült tábla egy 5x7-es mátrix            #
#-------------------------------------------------#
def read_from_file(fileName):

    #sourceFile = open(fileName, "r")
    sourceFile = open(fileName, encoding="utf8")
    #encoding="utf8"
    #print(sourceFile)
    readContent = sourceFile.read()
    sourceFile.close()
    
    table = [[0 for x in range(7)] for y in range(5)]
    for line in readContent.split('\n'):
        if line[0] != '#':
            lineParts = line.split('$')
            #print(len(lineParts))
            sub = SubjectInstance(lineParts[0], lineParts[1], lineParts[2],
                          lineParts[3], lineParts[4], lineParts[5],
                          lineParts[6])
            #sub.print_html_form()
            x = day_to_int(sub.day)
            y = begin_to_int(sub.begin)
            #print("day=" + sub.day + ":" + str(x) + " begin=" + sub.begin + ":" + str(y))
            if table[x][y] == 0:
                table[x][y] = [sub]
            else:
                table[x][y].append(sub)
    
    return table

#---------------------------------------------------------#
# Egy időpontra eső órák maximális számának meghatározása #
#---------------------------------------------------------#
def determine_max_subject_instance(table):
    print("Elemek száma időpontokra bontva:")
    maxLenInColumn = [0 for z in range(5)]
    for j in range(7):
        for i in range(5):
            if table[i][j] != 0:
                cntElements = len(table[i][j])
                sys.stdout.write(str(cntElements) + " ")
                if maxLenInColumn[i] < cntElements:
                    maxLenInColumn[i] = cntElements
            else:
                sys.stdout.write("0 ")
        print(" ")
        sys.stdout.flush()
    return maxLenInColumn


def main():    
    
    math = SubjectInstance("Alkalmazott matematika 1",
                   "PBANMEN01", "ea",
                   "Dr. Kovács István Béla, Dr. Baják Szabolcs, Gehér László",
                   "H", "09:40-11:10", "(III. Előadó);")
    math.value = 4
    #math.print_html_form()
        
    table = read_from_file("D:\\MyWorks\\python-gyak\\tansrc.txt")   
    maxLenInColumn = determine_max_subject_instance(table)

    print("Maxmimális elemszám naponként:") 
    print(maxLenInColumn)

    ##
    # HTML fájl összerakása
    ##

    thead = ""
    daysOfWeek = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]
    for i in range(5):
        thead += "<td colspan=\"" + str(maxLenInColumn[i]+1) + "\">" + daysOfWeek[i] + "</td> \r\n"

    tbody = ""
    for j in range(7):
        tbody += "<tr> \r\n"
        for i in range(5):
            if table[i][j] != 0:
                cntElements = len(table[i][j])
                for k in range(cntElements):
                    tbody += table[i][j][k].print_html_form()
                for k in range(maxLenInColumn[i] - cntElements+1):
                    tbody += print_blank_td()
            else:
                for k in range(maxLenInColumn[i]+1):
                    tbody += print_blank_td()
            tbody += "\r\n"
        tbody += "</tr> \r\n"
    
    strHTML = ('''
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                #kr2{	background-color: #00ff00	}
                #kr3{	background-color: #ffff00	}
                #kr4{	background-color: #ff8000	}
                #kr5{	background-color: #ff0000	}
                tr td
                {
                        border: 1px solid grey;
                        height: 80px;
                        text-align: center;
                }
                tr.thead td
                {
                        color: white;
                        text-align: center;
                        background-color: #57626a;
                        width: 300px;
                        height: 40px;
                }
                .ea
                {
                        border: 1px dashed black;
                        background-color: #ffaaaa
                }
                a
                {
                        text-decoration: none
                }

                h1 {
                padding: 15px;
                }

                h2,h3 {
                padding: 5px;
                }

                table {
                padding: 5px;
                }
            </style>
            <script>
                highlight = function(e) {
                    /**
                     * Meghatározom az egyes napokhoz tartozó oszlopok "szélességét" (colspan értékeket)
                     */
                    theadChildren = document.getElementsByClassName('thead')[0].children;
                    theadLens = [];
                    for (i = 0; i < theadChildren.length; ++i) {
                            val = parseInt(theadChildren[i].attributes['colspan'].value);
                            theadLens.push(val);
                    }
                    /**
                     * Kattintott elem sorszámának meghatározása (pontosabban: index száma)
                     */
                    parentChildren = e.parentElement.children;
                    index = 0;
                    while (index < parentChildren.length) {
                            if (e == parentChildren[index])
                                    break;
                            else
                                    ++index;
                            if (index == parentChildren.length)
                                    index = -1; //nincs tala'lat
                    }
                    /**
                     * Kummulálás a besoroláshoz
                     */
                    theadLensKum = [];
                    for (i = 0; i < theadLens.length; ++i) {
                            theadLensKum[i] = theadLens[i];
                            for (j = 0; j < i; ++j)
                                    theadLensKum[i] += theadLens[j];
                    }
                    /**
                     * Hét napjának indexének a meghatározása (a hét melyik napja alatt van a kattintott mező)
                     */
                    theadLenIndex = 0;
                    while(theadLenIndex < theadLens.length) {
                            if (index < theadLensKum[theadLenIndex])
                                    break;
                            else
                                    ++theadLenIndex;
                    }
                    /**
                     * Oszlophatárok kijelölése
                     */
                    b0 = 0;
                    b1 = theadLensKum[theadLensKum.length-1];
                    if (theadLenIndex != 0)
                            b0 = theadLensKum[theadLenIndex-1];
                    if (theadLenIndex != theadLens.length-1)
                            b1 = theadLensKum[theadLenIndex];
                    /**
                     * Kijelölt mező szélességének (colspan) módosítása, körülvevők elrejtése
                     */
                    newColSpanValue = b1-b0;
                    if (e.colSpan == newColSpanValue)
                            newColSpanValue = 1;
                    for (i = b0; i < b1; ++i) {
                            current = parentChildren[i];
                            if (current == e)
                                    current.colSpan = newColSpanValue;
                            else {
                                    newDisplayValue = "none";
                                    if (current.style.display == newDisplayValue)
                                            newDisplayValue = "";
                                    current.style.display = newDisplayValue;
                            }
                    }
                    /*
                    console.log(index);
                    console.log(theadLens);
                    console.log(theadLensKum);
                    console.log(theadLenIndex);
                    console.log(b0 + " " + b1);
                    */
                }            
            </script>
        </head>
        <body>
            <table>
                <tr class="thead"> ''' + thead + ''' </tr> ''' +
                tbody + '''
            </table>
        </body>
    </html>
    ''')
    
    ##
    # HTML fájl kiírása
    ##
    output = open("D:\\MyWorks\\python-gyak\\out.html", "w", encoding="utf8")
    output.write(strHTML)
    output.close()
                
main()
