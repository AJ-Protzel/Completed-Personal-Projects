library(shiny)
library(tidyverse)
library(leaflet)
library(htmlwidgets)

setwd("C:/Personal-Projects/NYC_covid")
all_modzcta <- readRDS("all_modzcta.RDS")

#Define UI for application
ui <- fluidPage(
  # Application title
  titlePanel("Covid-19 NYC Trends by Modified ZCTA"),
  # Sidebar with date input 
  sidebarLayout(
    sidebarPanel(
      tags$a(href="https://github.com/nychealth/coronavirus-data", "Data Repository",
      target = "blank"),
      h5("All data metrics are aggregated by week.
         Percent positive indicates percentage of people testes positive.
         All data is sourced from the NYC DoH."),
      selectInput("date",
                  "Select a date (week ending in):",
                  choices = unique(all_modzcta$week_ending)
                  )
      ),
      #Show a plot of the generated distribution
      mainPanel(
        tabsetPanel(
          tabPanel("Case Rate", leafletOutput("cases")),
          tabPanel("Test Rate", leafletOutput("tests")),
          tabPanel("Percent Positive", leafletOutput("pctpos"))
        )
      )
    )
)

# Define server logic
server <- function(input, output) {
  week_zcta <- reactive({
    w <- all_modzcta %>% filter(week_ending == input$date)
    return(w)
  })
  
  output$cases <- renderLeaflet({
    pal <- colorBin(palette = "YlGn", 9, domain = all_modzcta$caserate)
    
    labels = sprintf(
      "<strong>%s</strong><br/>%g cases per 100,000 people",
      week_zcta()$MODZCTA, week_zcta()$caserate) %>%
      lapply(htmltools::HTML)
    
    week_zcta() %>%
      st_transform(crs = "+init=epsg:4326") %>%
      leaflet() %>%
      addProviderTiles(provider = "CartoDB.Positron") %>%
      setView(-73.9, 40.7, zoom = 10) %>%
      addPolygons(label = labels,
                  stroke = FALSE,
                  smoothFactor = .5,
                  opacity = 1,
                  fillOpacity = .7, 
                  fillColor = ~ pal(week_zcta()$caserate),
                  highlightOptions = highlightOptions(weight = 5,
                                                      fillOpacity = 1,
                                                      color = "black",
                                                      opacity = 1,
                                                      bringToFront = TRUE)) %>%
      addLegend("bottomright",
                pal = pal,
                values = ~ caserate,
                title = "Cases Per 100,000",
                opacity = .7)
  })
  
  output$tests <- renderLeaflet({
    pal <- colorBin(palette = "PuBu", 9, domain = all_modzcta$testrate)
    
    labels = sprintf(
      "<strong>%s</strong><br/>%g cases per 100,000 people",
      week_zcta()$MODZCTA, week_zcta()$testrate) %>%
      lapply(htmltools::HTML)
    
    week_zcta() %>%
      st_transform(crs = "+init=epsg:4326") %>%
      leaflet() %>%
      addProviderTiles(provider = "CartoDB.Positron") %>%
      setView(-73.9, 40.7, zoom = 10) %>%
      addPolygons(label = labels,
                  stroke = FALSE,
                  smoothFactor = .5,
                  opacity = 1,
                  fillOpacity = .7, 
                  fillColor = ~ pal(week_zcta()$testrate),
                  highlightOptions = highlightOptions(weight = 5,
                                                      fillOpacity = 1,
                                                      color = "black",
                                                      opacity = 1,
                                                      bringToFront = TRUE)) %>%
      addLegend("bottomright",
                pal = pal,
                values = ~ testrate,
                title = "Tests Per 100,000",
                opacity = .7)
  })
  
  output$pctpos <- renderLeaflet({
    pal <- colorBin(palette = "OrRd", 9, domain = all_modzcta$pctpos)
    
    labels = sprintf(
      "<strong>%s</strong><br/>%g cases per 100,000 people",
      week_zcta()$MODZCTA, week_zcta()$pctpos) %>%
      lapply(htmltools::HTML)
    
    week_zcta() %>%
      st_transform(crs = "+init=epsg:4326") %>%
      leaflet() %>%
      addProviderTiles(provider = "CartoDB.Positron") %>%
      setView(-73.9, 40.7, zoom = 10) %>%
      addPolygons(label = labels,
                  stroke = FALSE,
                  smoothFactor = .5,
                  opacity = 1,
                  fillOpacity = .7, 
                  fillColor = ~ pal(week_zcta()$pctpos),
                  highlightOptions = highlightOptions(weight = 5,
                                                      fillOpacity = 1,
                                                      color = "black",
                                                      opacity = 1,
                                                      bringToFront = TRUE)) %>%
      addLegend("bottomright",
                pal = pal,
                values = ~ pctpos,
                title = "Tests Per 100,000",
                opacity = .7)
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
