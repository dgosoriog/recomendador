function datosArroz() {
  $('#datosArroz').empty();
  document.getElementById('prom_arroz').value = null;
  var a = document.getElementById("arroz").value;
  for (i = 0; i < a; i++) {
    var medArroz = document.createElement("input");
    medArroz.setAttribute("type", "number");
    medArroz.setAttribute("min", "0");
    medArroz.setAttribute("onblur", "calcPromArroz()");
    medArroz.setAttribute("class", "arroz");
    medArroz.setAttribute("placeholder", "Botón "+(i+1));
    medArroz.setAttribute("required", "True");
    medArroz.setAttribute("step","0.01");
    document.getElementById("datosArroz").appendChild(medArroz);
  }
}
function calcPromArroz(){
    var totArroz = 0;
    var contArroz = 0;
    $('.arroz').each(function() {
                        totArroz += parseFloat(this.value) || 0;
                        contArroz+=1;
                      });
    promA = totArroz/contArroz;
    document.getElementById('prom_arroz').value = promA.toFixed(2);
}

function datosArveja() {
  $('#datosArveja').empty();
  document.getElementById('prom_arveja').value = null;
  var arv = document.getElementById("arveja").value;
  for (i = 0; i < arv; i++) {
    var medArveja = document.createElement("input");
    medArveja.setAttribute("type", "number");
    medArveja.setAttribute("min", "0");
    medArveja.setAttribute("onblur", "calcPromArveja()");
    medArveja.setAttribute("class", "arveja");
    medArveja.setAttribute("placeholder", "Botón "+(i+1));
    medArveja.setAttribute("required", "True");
    medArveja.setAttribute("step","0.01");
    document.getElementById("datosArveja").appendChild(medArveja);
  }

}
function calcPromArveja(){
    var totArveja = 0;
    var contArveja = 0;
    $('.arveja').each(function() {
         totArveja += parseFloat(this.value) || 0;
         contArveja+=1;
         });
    promArv = totArveja/contArveja;
    document.getElementById('prom_arveja').value = promArv.toFixed(2);
}

function datosGarbanzo() {
  $('#datosGarbanzo').empty();
  var garb = document.getElementById("garbanzo").value;
  document.getElementById('prom_garb').value = null;
  for (i = 0; i < garb; i++) {
    var medGarbanzo = document.createElement("input");
    medGarbanzo.setAttribute("type", "number");
    medGarbanzo.setAttribute("min", "0");
    medGarbanzo.setAttribute("onblur", "calcPromGarbanzo()");
    medGarbanzo.setAttribute("class", "garbanzo");
    medGarbanzo.setAttribute("placeholder", "Botón "+(i+1));
    medGarbanzo.setAttribute("required", "True");
    medGarbanzo.setAttribute("step","0.01");
    document.getElementById("datosGarbanzo").appendChild(medGarbanzo);
  }
}
function calcPromGarbanzo(){
    var totGarb = 0;
    var contGarb = 0;
    $('.garbanzo').each(function() {
         totGarb += parseFloat(this.value) || 0;
         contGarb+=1;
         });
    promGarb = totGarb/contGarb;
    document.getElementById('prom_garb').value = promGarb.toFixed(2);
}

function datosLenteja() {
  $('#datosLenteja').empty();
  var lent = document.getElementById("lenteja").value;
  document.getElementById('prom_lenteja').value = null;
  for (i = 0; i < lent; i++) {
    var medLenteja = document.createElement("input");
    medLenteja.setAttribute("type", "number");
    medLenteja.setAttribute("min", "0");
    medLenteja.setAttribute("onblur", "calcPromLenteja()");
    medLenteja.setAttribute("class", "lenteja");
    medLenteja.setAttribute("placeholder", "Botón "+(i+1));
    medLenteja.setAttribute("required", "True");
    medLenteja.setAttribute("step","0.01");
    document.getElementById("datosLenteja").appendChild(medLenteja);
  }
}
function calcPromLenteja(){
    var totLenteja = 0;
    var contLenteja = 0;
    $('.lenteja').each(function() {
         totLenteja += parseFloat(this.value) || 0;
         contLenteja+=1;
         });
    promLent = totLenteja/contLenteja;
    document.getElementById('prom_lenteja').value = promLent.toFixed(2);
}

function datospcolor() {
  $('#datospcolor').empty();
  var pcolor = document.getElementById("pcolor").value;
  document.getElementById('prom_pcolor').value = null;
  for (i = 0; i < pcolor; i++) {
    var medpcolor = document.createElement("input");
    medpcolor.setAttribute("type", "number");
    medpcolor.setAttribute("min", "0");
    medpcolor.setAttribute("onblur", "calcPrompcolor()");
    medpcolor.setAttribute("class", "pcolor");
    medpcolor.setAttribute("placeholder", "Botón"+(i+1));
    medpcolor.setAttribute("required", "True");
    medpcolor.setAttribute("step","0.01");
    document.getElementById("datospcolor").appendChild(medpcolor);
  }
}
function calcPrompcolor(){
    var tot_pcolor = 0;
    var cont_pcolor = 0;
    $('.pcolor').each(function() {
         tot_pcolor += parseFloat(this.value) || 0;
         cont_pcolor+=1;
         });
    prom_pcolor = tot_pcolor/cont_pcolor;
    document.getElementById('prom_pcolor').value = prom_pcolor.toFixed(2);
}

function datosrcolor() {
  $('#datosrcolor').empty();
  var rcolor = document.getElementById("rcolor").value;
  document.getElementById('prom_rcolor').value = null;
  for (i = 0; i < rcolor; i++) {
    var medrcolor = document.createElement("input");
    medrcolor.setAttribute("type", "number");
    medrcolor.setAttribute("min", "0");
    medrcolor.setAttribute("onblur", "calcPromrcolor()");
    medrcolor.setAttribute("class", "rcolor");
    medrcolor.setAttribute("placeholder", "Botón "+(i+1));
    medrcolor.setAttribute("required", "True");
    medrcolor.setAttribute("step","0.01");
    document.getElementById("datosrcolor").appendChild(medrcolor);
  }
}
function calcPromrcolor(){
    var tot_rcolor = 0;
    var cont_rcolor = 0;
    $('.rcolor').each(function() {
         tot_rcolor += parseFloat(this.value) || 0;
         cont_rcolor+=1;
         });
    prom_rcolor = tot_rcolor/cont_rcolor;
    document.getElementById('prom_rcolor').value = prom_rcolor.toFixed(2);
}

function datoscolord() {
  $('#datoscolord').empty();
  var colord = document.getElementById("colord").value;
  document.getElementById('prom_colord').value = null;
  for (i = 0; i < colord; i++) {
    var medcolord = document.createElement("input");
    medcolord.setAttribute("type", "number");
    medcolord.setAttribute("min", "0");
    medcolord.setAttribute("onblur", "calcPromcolord()");
    medcolord.setAttribute("class", "colord");
    medcolord.setAttribute("placeholder", "Botón "+(i+1));
    medcolord.setAttribute("required", "True");
    medcolord.setAttribute("step","0.01");
    document.getElementById("datoscolord").appendChild(medcolord);
  }
}
function calcPromcolord(){
    var tot_colord = 0;
    var cont_colord = 0;
    $('.colord').each(function() {
         tot_colord += parseFloat(this.value) || 0;
         cont_colord+=1;
         });
    prom_colord = tot_colord/cont_colord;
    document.getElementById('prom_colord').value = prom_colord.toFixed(2);
}