
# Airbnb Market Analysis Tool
<p> Author : Ricardo Barbosa de Almeida Campos </p>

<img src  = "https://www.pieuvre.ca/wp-content/uploads/2019/06/Airbnb.jpg">

## Introduction
<p>This is an data science project that has as an objective to create a tool capable of providing fast statistical analysis for a large dataset and is interactive, so it can provided more flexible analysis with few clicks. </p>

## Business Problem
<p>This tool was created with a business problem in mind. The problem in question is that a business investor wants to start investing in real state, buy some properties and then starting renting those same properties. So, the investor requested a tool that is capable of doing a set of statistical analysis and using these tool, he will be capable of selecting the properties with the best financial return.</p>
<p>Some premises were taken into consideration before starting this project:
  <ul>
    <li> Properties with price set to zero are included in the analysis</li>
    <li> Properties with Availability set to 0 will considered inactive</li>
    <li> Most of the properties are in good condition</li>
    <li> For this scenario the investment to buy a house will be of U$ 1,000,000.00</li>
  </ul></p>

## Dataset
<p>The dataset was fetched in the following link :<a href = "https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data"> New York City Airbnb open data</a></p>
<p>A more detailed description of said dataset can be found in the link.</p>

## Business Solution
<p>As mentioned before, to help with the problem that investor is facing an interactive analysis tool was developed that is capable of filter data and present tables, plots and maps that can be used to choose the best buying opportunities.</p><p>For more accessibility, the tool will be available online and can be accessed anywhere the people responsible might need.</p>

## Data Feature

<p>For this tool, new variables were created to help with the decision making. Those variable were profitability and return of investment.
</p>

### Profitability

<p> This variable indicates how profitable the property is. Is a combination of price, the minimum nights required by who is offering the property to rent, the number of reviews that is an indicative of how many times the property was rented and Availability that indicates how many days a year this property is available to be rented.    
</p

![equation](http://www.sciweavers.org/download/Tex2Img_1658432952.jpg)

### Return of Investment

Return of investment indicates with how many rents the buyer will have the financial return of his investment.

![equation](http://www.sciweavers.org/download/Tex2Img_1658433225.jpg)


## Businees Insight
<p>During the development the interacitve tool, some insights that might the business team were found. They are as follow:
  <ul>
    <li> The New York region were properties were least available to be rented is Brooklyn</li>
    <li> The neighborhood with the most expensive rental on average is Fort Wadsworth </li>
    <li>The most profitable region is Manhattan</li>
  </ul></p>


   ### Tool Features
  <p> Some helpful features were developed, such as:
  <ul>
    <li> Only available properties can selected to be analyzed</li>
    <li> A table with selectable data can be ordered with the selected variable </li>
    <li> An aggregate table, with selectable variable on which to perform the aggregation, can be used to help compare regions or neighborhoods.</li>
  </ul>  
  </p>

  <p>The tool can be accessed using the following link :<a href = "https://house-rocket-analytics-ricardo.herokuapp.com/"> Analysis Tool</a></p>
