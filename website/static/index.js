// Value source: https://www.researchgate.net/publication/51076450/figure/tbl1/AS:601660669820932@1520458490045/Classification-of-physical-activity-according-to-the-intensity-of-METs.png (taken average for activities showing range)
function populate(sec1, sec2) {
  var s1 = document.getElementById(sec1);
  var s2 = document.getElementById(sec2);

  s2.innerHTML = "";
  var opts;

  if (s1.value == "light") {
    opts = [
      "|",
      "walking_slowly-2|Walking slowly (2)",
      "dish_washing-2|Dish washing (2)",
      "ironing-2|Ironing (2)",
      "making_beds-2|Making beds (2)",
      "work_at_desk-1.5|Work at desk (1.5)",
      "billiard-2.5|Billiard (2.5)",
      "dart-2.5|Dart (2.5)",
      "musical_instrument-2|Musical instrument (2)",
    ];
  } else if (s1.value == "moderate") {
    opts = [
      "|",
      "brisk_walking-3|Walking at brisk pace (3)",
      "washing_window-3|Washing window (3)",
      "sweeping_floor-3|Sweeping floor (3)",
      "badminton-4|Badminton (4)",
      "dancing-3.5|Dancing (3)",
      "light_bicycling-6|Bicycling-light (6)",
      "light_swimming-6|Swimming-light (6)",
      "tennis_double-8|Tennis-double (5)",
    ];
  } else if (s1.value == "vigorous") {
    opts = [
      "|",
      "jogging_running-6|Jogging/running (6)",
      "basketball-8|Basketball (8)",
      "soccer-8.5|Soccer (8.5)",
      "bicycling-8|Bicycling-moderate/high (8)",
      "swimming-9.5|Swimming-moderate/high (9.5)",
      "tennis-8|Tennis-single (8)",
    ];
  }

  for (var opt in opts) {
    var pair = opts[opt].split("|");
    var newopt = document.createElement("option");
    newopt.value = pair[0];
    newopt.innerHTML = pair[1];
    s2.options.add(newopt);
  }
}
