fetch("http://127.0.0.1:8000/analytics/model-registry")

.then(response => response.json())

.then(data=>{

document.getElementById("modelName").innerText=data.model_name;

document.getElementById("algorithm").innerText=data.algorithm;

document.getElementById("accuracy").innerText=data.accuracy+"%";

document.getElementById("status").innerText=data.status;

document.getElementById("version").innerText=data.version;

document.getElementById("dataset").innerText=data.dataset;



new Chart(

document.getElementById("accuracyChart"),

{

type:"doughnut",

data:{

labels:["Accuracy","Remaining"],

datasets:[{

data:[data.accuracy,100-data.accuracy]

}]

},

options:{

responsive:true,

maintainAspectRatio:false

}

}

);



new Chart(

document.getElementById("pipelineChart"),

{

type:"bar",

data:{

labels:[

"Collection",

"Cleaning",

"Training",

"Evaluation",

"Deployment"

],

datasets:[{

label:"Completion",

data:[100,100,100,100,100]

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

scales:{

y:{

beginAtZero:true,

max:100

}

}

}

}

);

});