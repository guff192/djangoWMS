let iframe = $("iframe")[0];
let iframe_src = iframe.src.split('/');
iframe_src.pop();

iframe_src = iframe_src.join('/') + '/';

let cells = $(".rack-empty, .pal-empty");
cells.each(function () {
    $(this).click(function () {
        let message = $(this).find("span.hidden").text();
        iframe.src = iframe_src + message;
        iframe.src = iframe.src;
    });
});

// cells.each(change)
    
