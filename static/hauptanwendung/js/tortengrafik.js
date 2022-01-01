     let ctx = document.getElementById("chart").getContext("2d");

     let chart = new Chart(ctx, {
         type: "doughnut",
         data: {
             labels: [
                 {% for antwort in antwort.frage.antwort_set.all %}
                 "{{ antwort }}",
                 {% endfor %}
             ],
             datasets: [
                 {
                     label: "Verteilung der Antworten",
                     backgroundColor: [
                         {% for antwort in antwort.frage.antwort_set.all %}"{% if antwort.richtig %}{{backgroundColorRichtig|index:forloop.counter0}}{% else %}{{backgroundColorFalsch|index:forloop.counter0}}{% endif %}",{% endfor %}                         
                     ],
                     borderColor: [
                         {% for antwort in antwort.frage.antwort_set.all %}"{% if antwort.richtig %}{{borderColorRichtig|index:forloop.counter0}}{% else %}{{borderColorFalsch|index:forloop.counter0}}{% endif %}",{% endfor %}                         
                     ],
                     data: [
                         {% for antwort in antwort.frage.antwort_set.all %}{{antwort.aufgerufen}},{% endfor %}                         
                     ]
                 }
             ]
         },
         options: {
             title: {
                 text: "Verteilung der Antworten",
                 display: true
             }
         }
     });
