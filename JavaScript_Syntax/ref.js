var x;
let y;
const z;
var list = [];
const object = {
    name : x,
    age: y,
    email: z
}

function func(){
    console.log(1);
}

(function iife() {
    console.log(1);
}());

let func1 = func;
func1();

let dom = document.getElementById();
document.getElementsByTagName();
document.getElementsByClassName();
document.querySelector();

console.log(dom.innerHTML)
dom.innerHTML = "Hello world";
dom.style.color = "red";

//---
document.getElementById("firstLine").innerHTML += " World";
let apples = document.getElementsByClassName("apple");
// let apples = document.querySelectorAll(".apple");
const color = ['red', 'blue', 'yellow', 'green', 'purple']
// apples.forEach(i => apples[i].innerHTML = "Not Apple");
for (let i = 0; i < apples.length; i++) {
    apples[i].style = `color:${color[i]};`;
}

//---
const ol = document.getElementsByTagName("ol")[0];
const array = ["xx", 2, 3, 4, 5];
array.forEach((name, index) => {
    ol.innerHTML += `<li>${name} at ${index}</li>`;
});
//---
const list = [1, 2, 3, 4, 5, 6, 7, 8, 9];

let result = list.filter(i => i % 2 == 0)
    .map(i => i * 10)
    .reduce((Accumulator, currentV) => Accumulator + currentV, 10);
console.log(result);

//---
function newFunc(){
    const name = "Garage";
    return function(){
        console.log(name);
    }
};

let secureFunc = newFunc();
secureFunc();



/*
Why can't I use forEach or map on a NodeList?
NodeList are used very much like arrays and it would be tempting to use Array.prototype methods on them. This is, however, impossible.

JavaScript has an inheritance mechanism based on prototypes. Array instances inherit array methods (such as forEach or map) because their prototype chain looks like the following:

myArray --> Array.prototype --> Object.prototype --> null (the prototype chain of an object can be obtained by calling several times Object.getPrototypeOf)

forEach, map and the likes are own properties of the Array.prototype object.

Unlike arrays, NodeList prototype chain looks like the following:

myNodeList --> NodeList.prototype --> Object.prototype --> null

NodeList.prototype contains the item method, but none of the Array.prototype methods, so they cannot be used on NodeLists.
*/
