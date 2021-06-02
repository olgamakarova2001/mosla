
 $(".moth p").click(function(){
       var $a = $(this).next(".daught");
       var t = $(this).text().slice(1,);
       var q = $(this).text().slice(0, 1);
       var $b = $(this);
       $(".innerdau").slideUp();
       $(".daught").not($a).slideUp();
       $a.slideToggle();
       if ( q == '▶'){
        $b.text("▼" + t);
       } else{
        $b.text("▶" + t);
       }
       $(".moth p").not($b).each(function(){
        $(this).text("▶" + $(this).text().slice(1,));
       });
       $(".innermo span").each(function(){
        $(this).text("▶" + $(this).text().slice(1,));
       });
       });


$(".innermo span").click(function(){
       var $a = $(this).next(".innerdau");
       var $b = $(this);
       var t = $(this).text().slice(1,);
       var q = $(this).text().slice(0, 1);
       $a.slideToggle();
       $(".innerdau").not($a).slideUp();
       if ( q == '▶'){
        $b.text("▼" + t);
       } else{
        $b.text("▶" + t);
       }
       $(".innermo span").not($b).each(function(){
        $(this).text("▶" + $(this).text().slice(1,));
       });
       });