(function () {
  "use strict";

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $all(selector, root) {
    return Array.from((root || document).querySelectorAll(selector));
  }

  async function loadJson(path) {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error("Failed to load " + path);
    }
    return response.json();
  }

  function uniqueSorted(values) {
    return Array.from(new Set(values.filter(Boolean))).sort(function (a, b) {
      return String(a).localeCompare(String(b));
    });
  }

  function fillSelect(select, values, placeholder) {
    select.innerHTML = "";
    const all = document.createElement("option");
    all.value = "";
    all.textContent = placeholder;
    select.appendChild(all);
    values.forEach(function (value) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  }

  function resourceHref(id) {
    return "../resource/" + id + ".html";
  }

  async function initExplore() {
    const tableBody = $("#explore-body");
    if (!tableBody) {
      return;
    }
    const catalog = await loadJson("../data/catalog.json");
    const resources = catalog.resources || [];
    const section = $("#filter-section");
    const layer = $("#filter-layer");
    const evidence = $("#filter-evidence");
    const kind = $("#filter-kind");
    const review = $("#filter-review");
    const query = $("#filter-query");
    const count = $("#result-count");

    fillSelect(section, uniqueSorted(resources.map(function (item) { return item.section; })), "All sections");
    fillSelect(
      layer,
      uniqueSorted(resources.flatMap(function (item) { return item.interoperability_layers || []; })),
      "All layers"
    );
    fillSelect(
      evidence,
      uniqueSorted(resources.flatMap(function (item) { return item.evidence_types || []; })),
      "All evidence"
    );
    fillSelect(kind, uniqueSorted(resources.map(function (item) { return item.resource_kind; })), "All kinds");
    fillSelect(review, uniqueSorted(resources.map(function (item) { return item.review_type; })), "All review types");

    function render() {
      const q = (query.value || "").trim().toLowerCase();
      const rows = resources.filter(function (item) {
        if (section.value && item.section !== section.value) return false;
        if (layer.value && !(item.interoperability_layers || []).includes(layer.value)) return false;
        if (evidence.value && !(item.evidence_types || []).includes(evidence.value)) return false;
        if (kind.value && item.resource_kind !== kind.value) return false;
        if (review.value && item.review_type !== review.value) return false;
        if (q) {
          const hay = [item.name, item.id, item.summary, item.mechanism, (item.connects || []).join(" ")]
            .join(" ")
            .toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });
      count.textContent = rows.length + " resource" + (rows.length === 1 ? "" : "s");
      tableBody.innerHTML = rows
        .map(function (item) {
          return (
            "<tr>" +
            '<td><a href="' + resourceHref(item.id) + '">' + item.name + "</a><div class=\"meta mono\">" + item.id + "</div></td>" +
            "<td>" + item.section + "</td>" +
            "<td>" + (item.interoperability_layers || []).join(", ") + "</td>" +
            "<td>" + (item.evidence_types || []).join(", ") + "</td>" +
            "<td>" + (item.review_type || "") + "</td>" +
            "</tr>"
          );
        })
        .join("");
    }

    [section, layer, evidence, kind, review, query].forEach(function (el) {
      el.addEventListener("input", render);
      el.addEventListener("change", render);
    });
    render();
  }

  async function initGraph() {
    const canvas = $("#graph-canvas");
    const select = $("#graph-root");
    if (!canvas || !select) {
      return;
    }
    const catalog = await loadJson("../data/catalog.json");
    const relations = await loadJson("../data/relations.json");
    const resources = catalog.resources || [];
    const byId = Object.fromEntries(resources.map(function (item) { return [item.id, item]; }));
    const edges = relations.edges || [];
    fillSelect(
      select,
      resources.map(function (item) { return item.id; }),
      "Select a resource"
    );
    const preferred = ["ro-crate", "flexible-image-transport-system-fits", "neurodata-without-borders-nwb"];
    preferred.some(function (id) {
      if (byId[id]) {
        select.value = id;
        return true;
      }
      return false;
    });

    const ctx = canvas.getContext("2d");
    let nodes = [];
    let links = [];

    function neighborhood(rootId) {
      const keep = new Set([rootId]);
      const local = [];
      edges.forEach(function (edge) {
        if (edge.source === rootId || edge.target === rootId) {
          keep.add(edge.source);
          keep.add(edge.target);
          local.push(edge);
        }
      });
      return {
        nodes: Array.from(keep).filter(function (id) { return byId[id]; }).map(function (id) {
          return { id: id, name: byId[id].name, root: id === rootId };
        }),
        links: local,
      };
    }

    function layout() {
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      canvas.width = width * window.devicePixelRatio;
      canvas.height = height * window.devicePixelRatio;
      ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
      const cx = width / 2;
      const cy = height / 2;
      const radius = Math.min(width, height) * 0.34;
      nodes.forEach(function (node, index) {
        if (node.root) {
          node.x = cx;
          node.y = cy;
          return;
        }
        const angle = (Math.PI * 2 * (index - 1)) / Math.max(nodes.length - 1, 1);
        node.x = cx + Math.cos(angle) * radius;
        node.y = cy + Math.sin(angle) * radius;
      });
    }

    function draw() {
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      ctx.clearRect(0, 0, width, height);
      const byNode = Object.fromEntries(nodes.map(function (node) { return [node.id, node]; }));
      ctx.strokeStyle = "#c7c1b4";
      ctx.lineWidth = 1.25;
      links.forEach(function (edge) {
        const a = byNode[edge.source];
        const b = byNode[edge.target];
        if (!a || !b) return;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      });
      nodes.forEach(function (node) {
        ctx.beginPath();
        ctx.fillStyle = node.root ? "#0f6e56" : "#fffdf8";
        ctx.strokeStyle = "#0f6e56";
        ctx.lineWidth = 2;
        ctx.arc(node.x, node.y, node.root ? 18 : 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "#13202b";
        ctx.font = "14px Source Sans 3, sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(node.name, node.x, node.y + (node.root ? 34 : 28));
      });
    }

    function render() {
      const rootId = select.value;
      const meta = $("#graph-meta");
      if (!rootId) {
        nodes = [];
        links = [];
        draw();
        if (meta) meta.textContent = "Choose a resource to inspect its typed relation neighborhood.";
        return;
      }
      const graph = neighborhood(rootId);
      nodes = graph.nodes;
      links = graph.links;
      layout();
      draw();
      if (meta) {
        meta.innerHTML =
          "Neighborhood for <a href=\"" +
          resourceHref(rootId) +
          "\">" +
          byId[rootId].name +
          "</a>: " +
          links.length +
          " edge" +
          (links.length === 1 ? "" : "s") +
          ", " +
          nodes.length +
          " nodes.";
      }
    }

    select.addEventListener("change", render);
    window.addEventListener("resize", function () {
      layout();
      draw();
    });
    canvas.addEventListener("click", function (event) {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const hit = nodes.find(function (node) {
        const dx = node.x - x;
        const dy = node.y - y;
        return Math.sqrt(dx * dx + dy * dy) <= (node.root ? 18 : 12);
      });
      if (hit) {
        window.location.href = resourceHref(hit.id);
      }
    });
    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initExplore().catch(function (error) {
      const count = $("#result-count");
      if (count) count.textContent = String(error);
    });
    initGraph().catch(function (error) {
      const meta = $("#graph-meta");
      if (meta) meta.textContent = String(error);
    });
  });
})();
