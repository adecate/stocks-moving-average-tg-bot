# stocks-moving-average-tg-bot 
Я сделал этого бота во время прохождения курса (https://www.coursera.org/learn/python-statistics-financial-analysis) для автоматизации такого инструмента технического анализа как simple moving average (MA). 
Суть метода:
На основании определенного периода выстраивается прямая, сглаживающая ценовые вспелски, указывая на текущую тенденцию. 
Мы будем выстраивать две прямые: одну для бОльшего периода [MA100], другую для меньшего [MA10].
Существует мнение, что цена вернется к своему среднему значению (в краткосрочном периоде), это значит, что если в текущий момент линяя, описывающая [MA10] ниже линии, описывающей [MA100], значит цена скорректируется к среднему значению (возрастет).
И наоборот. 
