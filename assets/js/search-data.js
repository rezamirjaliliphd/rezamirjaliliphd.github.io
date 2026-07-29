// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "publications",
          description: "Peer-reviewed articles, preprints, and work in progress, in reverse chronological order. Also on Google Scholar and ORCID.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "Research on exact and learning-augmented optimization, alongside applied machine learning work.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-code",
          title: "code",
          description: "Open-source work I can share publicly — applied machine learning, reinforcement learning, and this site. Research code from my dissertation is kept private.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/repositories/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "Education, research experience, publications, and technical skills. The PDF version is linked from the icon on the right.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "news-earned-the-nvidia-certifications-in-cuda-c-c-programming-and-deep-learning-fundamentals",
          title: 'Earned the NVIDIA certifications in CUDA C/C++ Programming and Deep Learning Fundamentals.',
          description: "",
          section: "News",},{id: "news-completed-the-mlops-and-llmops-specializations-at-duke-university",
          title: 'Completed the MLOps and LLMOps specializations at Duke University.',
          description: "",
          section: "News",},{id: "news-defended-and-completed-my-ph-d-in-industrial-engineering-at-the-university-of-houston-tada",
          title: 'Defended and completed my Ph.D. in Industrial Engineering at the University of Houston....',
          description: "",
          section: "News",},{id: "news-new-preprint-on-arxiv-resource-based-time-and-cost-prediction-in-project-networks-applying-graph-neural-networks-to-project-scheduling",
          title: 'New preprint on arXiv: Resource-Based Time and Cost Prediction in Project Networks, applying...',
          description: "",
          section: "News",},{id: "projects-cnn-hyperparameter-search-on-cifar-10",
          title: 'CNN hyperparameter search on CIFAR-10',
          description: "Optuna-driven tuning of a convolutional network, optimising for search efficiency rather than raw accuracy.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/cnn-hyperparameter-search/";
            },},{id: "projects-learning-cutting-planes",
          title: 'learning cutting planes',
          description: "Deep Q-learning for generating Chvátal–Gomory cuts, plus a hybrid inequality family.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/learning-cutting-planes/";
            },},{id: "projects-learning-to-price",
          title: 'learning to price',
          description: "Deep reinforcement learning for prioritizing pricing subproblems inside column generation.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/learning-to-price/";
            },},{id: "projects-stock-price-forecasting-with-lstm",
          title: 'stock price forecasting with LSTM',
          description: "An LSTM trained on eight years of AAPL data, judged on direction rather than on loss.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/lstm-stock-forecasting/";
            },},{id: "projects-mothership-amp-drone-routing",
          title: 'mothership &amp;amp; drone routing',
          description: "An exact branch-and-price-and-cut algorithm for coordinating a support vehicle with a fleet of delivery drones.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/mothership-drone-routing/";
            },},{id: "projects-network-resilience-after-snow-storms",
          title: 'network resilience after snow storms',
          description: "Measuring and forecasting how New York City&#39;s transportation network recovers from winter storms.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/network-resilience/";
            },},{id: "projects-project-networks-with-graph-neural-networks",
          title: 'project networks with graph neural networks',
          description: "Predicting project duration and cost from activity–resource graphs, beyond CPM and PERT.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/project-networks-gnn/";
            },},{id: "projects-q-learning-for-shortest-paths",
          title: 'Q-learning for shortest paths',
          description: "Reinforcement learning on a constrained grid graph, as a bridge between RL and combinatorial optimization.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/qlearning-shortest-path/";
            },},{id: "projects-english-to-french-translation-with-t5",
          title: 'English-to-French translation with T5',
          description: "Fine-tuning T5-small on OPUS Books with mixed-precision training.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/t5-translation/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%72%65%7A%61.%6D%69%72%6A%61%6C%69%6C%69@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/rezamirjaliliphd", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/rezamirjalili", "_blank");
        },
      },{
        id: 'social-orcid',
        title: 'ORCID',
        section: 'Socials',
        handler: () => {
          window.open("https://orcid.org/0000-0002-5228-061X", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=xKo0UD0AAAAJ", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
