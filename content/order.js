window.__G = { tabs: {}, order: ["basic","structure","menus","contents","units","tips","notes600","links","images"] };
document.write(window.__G.order.map(function (id) { return '<script src="content/' + id + '.js"><\/script>'; }).join(""));
