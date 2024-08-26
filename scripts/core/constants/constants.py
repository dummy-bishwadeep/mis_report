
sample_output = {
  "widgetId": "DDicME5JYcZeLFMhMdKvqn",
  "chartData": {
    "xAxis": {
      "type": "category",
      "data": [
        "Oxygen Variation, Low O2 and High O2",
        "Others",
        "Process Start Up / Plant Stop"
      ]
    },
    "yAxis": [
      {
        "type": "value",
        "yAxisIndex": 0,
        "axisLabel": {
          "formatter": "{value}"
        }
      },
      {
        "type": "value",
        "yAxisIndex": 1,
        "axisLabel": {
          "formatter": "{value} %"
        }
      }
    ],
    "series": [
      {
        "name": "MTD",
        "color": "#4472C4",
        "type": "bar",
        "yAxisIndex": 1,
        "data": [
          [
            "Oxygen Variation, Low O2 and High O2",
            48.85
          ],
          [
            "Others",
            7.41
          ],
          [
            "Process Start Up / Plant Stop",
            4.12
          ]
        ]
      },
      {
        "name": "Percentage",
        "color": "#ED7C2F",
        "showSymbol": False,
        "type": "line",
        "yAxisIndex": 0,
        "smooth": True,
        "data": [
          [
            "Process Start Up / Plant Stop",
            6.0
          ],
          [
            "Others",
            12.0
          ],
          [
            "Oxygen Variation, Low O2 and High O2",
            80.0
          ]
        ]
      }
    ]
  },
  "statistics": None,
  "data_stats": {},
  "queryRange": {
    "from": 1711909800000,
    "to": 1719685799999
  },
  "qC": {}
}

TIMEZONE = "Asia/Kolkata"

paremeter_list = ["l1_100$l2_101$l3_102$l4_103$l5_104$a_123$tag_102",
                  "l1_100$l2_101$l3_102$l4_103$l5_104$a_123$tag_104",
                  "l1_100$l2_101$l3_102$l4_103$l5_104$a_123$tag_103",
                  "l1_100$l2_101$l3_102$l4_103$l5_104$a_123$tag_107"]

agg = "avg"

sampling = {"days": "Days",
            "day": "Days",
            "months": "Months",
            "month": "Months",
            "year": "Years",
            "years": "Years",
            "week": "Weeks",
            "weeks": "Weeks",
            "yesterday": "Days",
            "today": "Days",
            "minutes": "Minutes",
            "minute": "Minutes",
            "hour": "Hours",
            "hours": "Hours",
            }