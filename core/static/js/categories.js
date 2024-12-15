showProjectButton = document.getElementById("showProjectCard");
hideProjectButton = document.getElementById("hideProjectCard");
ProjectCard = document.getElementById("ProjectCard");

showProjectButton.addEventListener("click",  showProject);
hideProjectButton.addEventListener("click",  hideProject);


showCategoryButton = document.getElementById("showPCCard");
hideCategoryButton = document.getElementById("hidePCCard");
PCCard=document.getElementById("addProjectCategory");

showCategoryButton.addEventListener("click", showCategory);
hideCategoryButton.addEventListener("click", hideCategory);


function showProject(){
    ProjectCard.style.left = `calc(50% - 200px)`;
    PCCard.style.left = `-100%`;
};
// alert("he")

function hideProject(){
    ProjectCard.style.left = `-100%`;
};




function showCategory(){
    PCCard.style.left = `calc(50% - 200px)`;
    ProjectCard.style.left = `-100%`;
};
function hideCategory(){
    PCCard.style.left = `-100%`;
};

// alert("He")