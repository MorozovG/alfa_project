#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggplot2)
library(dplyr)

data <- read_csv('/Users/morozovgleb/Documents/alfa_project/process_data/data_plot.csv')
data <- data %>% mutate(year = format(review_datetime, "%Y"), 
                        month = format(review_datetime, "%m"), day = format(review_datetime, "%d"))

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  textVals <- eventReactive(input$submit, {
    input$variable
  })
  
  output$text <- renderText({
    category_names_rus <-  list(autocredits = "Автокредиты",
                                businesscredits = "Кредитование бизнеса",
                                businessdeposits = "Депозиты для бизнеса",
                                corporate = "Обслуживание юрлиц",
                                creditcards = "Кредитные карты",
                                credits = "Потребительские кредиты",
                                debitcards = "Дебетовые карты",
                                deposits = "Вклады",
                                hypothec = "Ипотечные кредиты",
                                leasing = "Лизинг",
                                remote = "Дистанционное обслуживание",
                                restructing = "Реструктуризация кредитов")
    request_url <- "/Users/morozovgleb/anaconda/bin/python /Users/morozovgleb/Documents/alfa_project/test_string.py"
    request_text <- paste('"', textVals(), '"', sep = '')
    categories <- system(paste(request_url, request_text), intern = T)
    categories_rus <- unlist(category_names_rus[categories], use.names = FALSE)
    paste(categories_rus, collapse = ",   ")
    #system("/Users/morozovgleb/anaconda/bin/python /Users/morozovgleb/Documents/alfa_project/test.py", intern = T)
    #getwd()
    
    })
  #filtered <- reactive({data <- data %>% filter(year <= input$year[2])})
  filtered <- reactive({
    if (input$predicted == "No") {
      data <- data %>% filter(category_check == 1)
      }
    if (input$raiting != "All") {
      data <- data %>% filter(review_rating == input$raiting)
    }
    if (input$category != "All") {
      data <- data %>% filter_(paste(input$category, "==", 1))
    }
    
    data %>% filter(year <= input$year[2],
                    year >= input$year[1],
                    bank_name == input$bank) %>%
      group_by(year_t = format(review_datetime, "%Y-%U")) %>% 
      summarise(num_reviews = n())
    #data %>% filter(bank_name == input$bank)
  })
  # output$test <- renderText(nrow(filtered()))
  output$coolplot <- renderPlot({
    ggplot(filtered(), aes(year_t, num_reviews, group = 1)) + geom_line() +
      geom_smooth() + xlab("Weeks") + ylab("Number of reviews")
    
    
  })
  
})
