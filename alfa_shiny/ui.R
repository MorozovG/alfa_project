#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
shinyUI(navbarPage("Alfa project",
  tabPanel("Category prediction",
  # Application title
  titlePanel("Определение категорий отзыва"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(width = 5,
       h4("Категории"),
       textOutput("text")
    ),
    
    # Show a plot of the generated distribution
    mainPanel(width = 7,
      textAreaInput("variable", "Введите отзыв", "", width = "800px", height = "400px"),
      actionButton("submit", "Submit")
    )
  ),
  br(), br(), br(),
  "Модель классифицирует введённый отзыв по 12 категориям. Набор возможных категорий взят с сайта",
  a("Banki.ru.", href = "http://www.banki.ru/services/responses/bank/alfabank/"),
  "Каждая категория представляет собой услугу предоставляемую банком.",
  "Классы отзывов взаимно пересекаются, поэтому возможна классификация отзыва одновременно для нескольких категорий."
),
tabPanel("Plot",
         sidebarLayout(
           sidebarPanel(width = 3,
             sliderInput("year", "Year", 2005, 2017, value = c(2005, 2017)),
             selectInput("bank", "Bank name",
                         c('alfabank', 'avangard', 'binbank', 'fk_otkritie', 'raiffeisen',
                           'sberbank', 'tcs')),
             selectInput("category", "Category name",
                         c('All', 'autocredits', 'businesscredits', 'businessdeposits',
                           'corporate', 'creditcards', 'credits', 'debitcards', 'deposits', 'hypothec',
                           'leasing', 'remote', 'restructing')),
             selectInput("predicted", "With predicted category",
                         c("Yes", "No")),
             selectInput("raiting", "Rating by review",
                         c("All", 1, 2, 3, 4, 5))
             
           ),
           mainPanel(width = 9, plotOutput("coolplot", height = "800px"),
                     textOutput("test")
             
           )
         ))
))
