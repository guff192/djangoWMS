if (location.pathname == "/wms/map/") {
    let iframe = $("iframe#info_bar");

    let iframe_src = iframe[0].src.split("/");
    iframe_src.pop();
    iframe_src = iframe_src.join("/") + "/";
    
    iframe[0].addEventListener("load", function () {
        iframe.contents().find(".header").addClass("hidden");
    });

    $(".rack, .pal, .rack-empty, .pal-empty").each(function () {
        $(this).click(function () {
            let message = $(this).find("span.hidden").text();
            iframe[0].src = iframe_src + message;

            $(".selected").each(function () {
                this.classList.remove("selected");
            })
            this.classList.add("selected");
            
            $("iframe").contents().find(".header").css("display", "none");
        });
    });
}

    
