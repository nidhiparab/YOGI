document.addEventListener("DOMContentLoaded", ()=>{
    const gender = instantiateGender();
    let splitUrl = window.location.href.split("/");
    let sectionFromUrl = splitUrl[splitUrl.length - 2];
    let sectionMenuChildrenArray = Array.from(document.getElementsByClassName("js-section-button"));
    sectionMenuChildrenArray.forEach(element=>{
        let elmMatches = element.innerText.trim().toUpperCase().includes(sectionFromUrl.toUpperCase());
        if (elmMatches) {
            localStorage.setItem("section", element.innerText.trim().charAt(0) + element.innerText.trim().slice(1).toLowerCase());
        }
    }
    );
    let section = localStorage.getItem("section") ?? "Exercises";
    $(".js-sex-option").on("change", (e)=>{
        showGenderSelection(e.target.value);
    }
    );
    $("#body-map").on("click", (event)=>{
        const bodyPart = event.target.parentElement.id;
        const navigationPath = buildNavigationPath(bodyPart, section);
        if (navigationPath) {
            window.location = '/' + navigationPath;
        }
    }
    );
    $(`#sexchooser${gender}label`).click();
    document.onclick = ()=>{
        $moreMenu.removeClass("more-menu--open");
        $mobileMenu.removeClass("mobile-menu--open");
    }
    ;
    var $moreMenu = $(".js-more-menu")
      , $mobileMenu = $(".js-mobile-menu")
      , $mobileMenuToggle = $('.js-mobile-menu-toggle')
      , $mobileToggleLabel = $(".js-toggle-button-label")
      , $showMoreButton = $(".js-show-more-button")
      , $showMoreButtonLabel = $(".js-category-display")
      , optDeselect = false;
    section = section.toLowerCase();
    $(".section-selected").removeClass("section-selected");
    $(`[data-js-section="${section}"]`).addClass("section-selected");
    let selectedText = $(".section-selected").first().text();
    $mobileToggleLabel.text(selectedText || "Featured");
    if ($(".section-selected").hasClass("more-menu-opt")) {
        $showMoreButton.addClass("section-selected");
        $showMoreButtonLabel.text(selectedText);
    }
    $mobileMenuToggle.on("click", (e)=>{
        $mobileMenu.toggleClass("mobile-menu--open");
        e.stopPropagation();
    }
    );
    $(".js-section-button").on("click", (e)=>{
        let $button = $(e.target)
          , oldSection = localStorage.getItem("section")
          , newSection = $button.data("js-section");
        optDeselect = false;
        $showMoreButtonLabel.text("More");
        $mobileMenuToggle.addClass('mobile-menu-toggle--section-selected')
        $(".section-selected").removeClass("section-selected");
        localStorage.removeItem("section");
        $mobileToggleLabel.text("Featured");
        if (newSection === oldSection) {
            optDeselect = true;
            $showMoreButton.removeClass("section-selected");
            $mobileMenuToggle.removeClass('mobile-menu-toggle--section-selected')
            return;
        }
        $mobileToggleLabel.text($button.text());
        $button.addClass("section-selected");
        section = newSection;
        localStorage.setItem("section", newSection);
    }
    );
    $(".js-more-menu-opt").on("click", (e)=>{
        if (optDeselect) {
            return;
        }
        $showMoreButton.addClass("section-selected");
        $showMoreButtonLabel.text($(e.target).text());
    }
    );
    $showMoreButton.on("click", (e)=>{
        $moreMenu.toggleClass("more-menu--open");
        e.stopPropagation();
    }
    );
}
);
function instantiateGender() {
    let gender = localStorage.getItem("sex");
    if (gender !== "male" && gender !== "female") {
        localStorage.setItem("sex", "male");
        gender = "male";
    }
    return gender;
}
function showGenderSelection(gender) {
    const bodyMapContainer = $("#body-map");
    const maleBodyMap = $("#male-body-maps");
    const femaleBodyMap = $("#female-body-maps");
    maleBodyMap.hide();
    femaleBodyMap.hide();
    bodyMapContainer.removeClass('invisible');
    switch (gender) {
    case "female":
        {
            localStorage.setItem("sex", "female");
            femaleBodyMap.fadeIn(500);
            break;
        }
    case "male":
        {
            $('#body-map').removeClass('hidden');
            localStorage.setItem("sex", "male");
            maleBodyMap.fadeIn(500);
            break;
        }
    default:
        {
            $('#body-map').removeClass('hidden');
            localStorage.setItem("sex", "male");
            maleBodyMap.fadeIn(500);
            break;
        }
    }
}
function buildNavigationPath(bodyPart, section) {
    const validBodyParts = ["calves", "quads", "traps", "shoulders", "biceps", "triceps", "forearms", "lowerback", "hamstrings", "obliques", "chest", "abdominals", "quads", "lats", "glutes", "traps_middle", ];
    if (validBodyParts.includes(bodyPart)) {
        const gender = localStorage.getItem("sex");
        return [section, gender, bodyPart].join("/");
    }
}