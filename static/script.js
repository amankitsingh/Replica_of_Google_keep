var cards = document.getElementsByClassName('card');
for (i = 0; i < cards.length; ++i) {
    (function (i) {
        cards[i].addEventListener("mouseover", function (event) {

            document.getElementsByClassName("card-edit")[i].style.visibility = "visible";
            document.getElementsByClassName("card-done")[i].style.visibility = "visible";
        });
        cards[i].addEventListener("mouseout", function () {
            document.getElementsByClassName("card-edit")[i].style.visibility = "hidden";
            document.getElementsByClassName("card-done")[i].style.visibility = "hidden";
        });
    })(i);
}

document.getElementsByClassName("container")[0].addEventListener("click", function () {
    document.getElementsByClassName("side-nav")[0].style.visibility = "hidden";
});

var isMobile = 0;
onResize();

function onResize() {
    if (window.innerWidth <= 767) {
        isMobile = 1;
    } else {
        isMobile = 0;
    }
}

function clearSearch() {
    document.getElementsByClassName('search')[0].value = "";
}

function showSearch() {
    document.getElementsByClassName('side-nav')[0].style.display = "none";
    if (isMobile == 1) {
        document.getElementsByClassName('nav-right')[0].style.display = "none";
        document.getElementById('menu-icon').style.display = "none";
        document.getElementById('logo').style.display = "none";
        document.getElementById('search-icon').style.display = "none";
        document.getElementById('search').style.display = "inline-block";
        document.getElementById('search').style.width = "90%";
        document.getElementById('search').style.position = "relative";
        document.getElementById('search').style.left = "50%";
        document.getElementById('search').style.marginLeft = "-45%";

        document.getElementsByClassName('search')[0].style.margin = "0px";
        document.getElementsByClassName('search')[0].style.padding = "0px";
        document.getElementsByClassName('search')[0].style.paddingLeft = "20px";
        document.getElementsByClassName('search')[0].style.marginLeft = "-12px";
        document.getElementsByClassName('search')[0].style.width = "100%";
        document.getElementsByClassName('search')[0].focus();
        document.getElementById('close-search').style.position = "absolute";
        document.getElementById('close-search').style.display = "inline-block";
        document.getElementById('close-search').style.right = "10px";
    } else {
        document.getElementById('close-search').style.display = "inline-block";
    }
}

function searchnote(elem) {
    var input, filter, ul, li, a, i, txtValue;
    filter = elem.toUpperCase();
    ul = document.getElementsByClassName("search-item");
    for (i = 0; i < ul.length; i++) {
        a = ul[i].innerText.toUpperCase();
        if (a == filter) {
            k = ul[i].style.color = "yellow";
        }
    }
    if (filter == "") {
        k = document.getElementsByClassName("search-item");
        for (i = 0; i < ul.length; i++) {
            console.log(k[i].innerText);
            k[i].style.color = "black";
        }
    }
}

function showSideNav() {
    document.getElementsByClassName('side-nav')[0].style.display = "block";
}

function removeSearch() {
    if (isMobile == 1) {
        document.getElementsByClassName('nav-right')[0].style.display = "inline-block";
        document.getElementById('menu-icon').style.display = "inline-block";
        document.getElementById('logo').style.display = "inline-block";
        document.getElementById('search-icon').removeAttribute('style');
        document.getElementById('search').removeAttribute('style');
        document.getElementsByClassName('search')[0].removeAttribute('style');
        document.getElementById('close-search').removeAttribute('style');
    } else {
        document.getElementById('close-search').style.display = "none";
    }
}

function textnote() {
    document.getElementsByClassName('listmenu')[0].style.visibility = "hidden";
    document.getElementById('textInput').className = "show";
    document.getElementById('textbutton').className = "showbutton";
    document.getElementsByClassName('linknote')[0].style.visibility = "hidden";
    document.getElementsByClassName('flex-container')[0].style.visibility = "hidden";
    document.getElementsByClassName('maplink')[0].style.visibility = "hidden";
}

function listnote() {
    document.getElementsByClassName('listmenu')[0].style.visibility = "visible";
    document.getElementById('textInput').className = "hide";
    document.getElementById('textbutton').className = "hide";
    document.getElementsByClassName('linknote')[0].style.visibility = "hidden";
    document.getElementsByClassName('flex-container')[0].style.visibility = "hidden";

    document.getElementsByClassName('maplink')[0].style.visibility = "hidden";
}

function linknote() {
    document.getElementsByClassName('linknote')[0].style.visibility = "visible";
    document.getElementsByClassName('listmenu')[0].style.visibility = "hidden";
    document.getElementById('textInput').className = "hide";
    document.getElementById('textbutton').className = "hide";
    document.getElementsByClassName('flex-container')[0].style.visibility = "hidden";
    document.getElementsByClassName('maplink')[0].style.visibility = "hidden";
}

function maplink() {
    document.getElementsByClassName('maplink')[0].style.visibility = "visible";
    document.getElementsByClassName('flex-container')[0].style.visibility = "hidden";
    document.getElementsByClassName('linknote')[0].style.visibility = "hidden";
    document.getElementsByClassName('listmenu')[0].style.visibility = "hidden";
    document.getElementById('textInput').className = "hide";
    document.getElementById('textbutton').className = "hide";
}

var myNodeclass = document.getElementsById("myUL");
myNodelist = myNodeClass.querySelector("li");
for (var i = 0; i < myNodelist.length; i++) {
    var span = document.createElement("SPAN");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
}


var cl = document.getElementsByClassName("close");
for (i = 0; i < cl.length; i++) {
    cl[i].onclick = function () {
        var div = this.parentElement;
        div.style.display = "none";
    };
}
var list = myNodelist;
list.addEventListener('click', function (ev) {
    if (ev.target.tagName === 'li') {
        ev.target.classList.toggle('checked');
    }
}, false);

function newElement() {
    var li = document.createElement("li");
    var inputValue = document.getElementById("myInput").value;
    var t = document.createTextNode(inputValue);
    li.appendChild(t);
    if (inputValue === '') {
        alert("You must write something!");
    } else {
        document.getElementById("myUL").appendChild(li);
    }
    document.getElementById("myInput").value = "";

    var span = document.createElement("SPAN");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    li.appendChild(span);

    var close = document.getElementsByClassName("close");
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            var div = this.parentElement;
            div.style.display = "none";
        };
    }
}