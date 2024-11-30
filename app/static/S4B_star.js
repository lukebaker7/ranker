// S4B_star.js
function starry (instance) {
  // (A) SET DEFAULTS
  if (instance.max === undefined) { instance.max = 5; }
  if (instance.now === undefined) { instance.now = 0; }
  if (instance.now > instance.max) { instance.now = instance.max; }
  if (instance.disabled === undefined) { instance.disabled = false; }

  // (B) GENERATE STARS
  instance.target.classList.add("starwrap");
  for (let i=1; i<=instance.max; i++) {
    // (B1) CREATE HTML STAR
    let s = document.createElement("div");
    s.className = "star";
    let icon = document.createElement("i");
    icon.className = "fas fa-star";
    s.appendChild(icon);
    instance.target.appendChild(s);

    // (B2) HIGHLIGHT STAR
    if (i <= instance.now) { 
        s.classList.add("on"); 
    }

    if (!instance.disabled) {
      // (B3) ON MOUSE OVER
      s.onmouseover = () => {
        let all = instance.target.getElementsByClassName("star");
        for (let j=0; j<all.length; j++) {
          if (j<i) { all[j].classList.add("on"); }
          else { all[j].classList.remove("on"); }
        }
      };

      // (B4) ON MOUSE LEAVE
      instance.target.onmouseleave = () => {
        let all = instance.target.getElementsByClassName("star");
        for (let j=0; j<all.length; j++) {
          if (j<instance.now) { all[j].classList.add("on"); }
          else { all[j].classList.remove("on"); }
        }
      };

      // (B5) ON CLICK
      if (instance.click) { s.onclick = () => instance.click(i); }
    }
  }
}