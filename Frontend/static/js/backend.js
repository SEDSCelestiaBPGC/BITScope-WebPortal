document.addEventListener('DOMContentLoaded', function() {
    // Example: Add event listeners for buttons or forms
    const observeButtons = document.querySelectorAll('.observe');
    observeButtons.forEach(button => {
        button.addEventListener('click', function() {
            $('#popup').modal('show');
        });

        // GSAP animation for Observe buttons
        button.addEventListener('mouseenter', function() {
            gsap.to(button.querySelector('.fill'), {
                duration: 0.5,
                width: '100%',
                ease: "power2.out"
            });
        });

        button.addEventListener('mouseleave', function() {
            gsap.to(button.querySelector('.fill'), {
                duration: 0.5,
                width: '0',
                ease: "power2.out"
            });
        });
    });

    // GSAP animation for the About Observatory button
    const aboutButton = document.getElementById('about-button');

    aboutButton.addEventListener('mouseenter', function() {
        gsap.to(aboutButton, {
            duration: 0.1,
            backgroundColor: "#007bff",
            color: "#fff",
            borderRadius: "10px",
            ease: "power2.out"
        });
    });

    aboutButton.addEventListener('mouseleave', function() {
        gsap.to(aboutButton, {
            duration: 0.1,
            backgroundColor: "transparent",
            color: "#007bff",
            borderRadius: "0px",
            ease: "power2.out"
        });
    });

    // GSAP animation for the Team button
    const teamButton = document.getElementById('team-button');

    teamButton.addEventListener('mouseenter', function() {
        gsap.to(teamButton, {
            duration: 0.1,
            backgroundColor: "#007bff",
            color: "#fff",
            borderRadius: "10px",
            ease: "power2.out"
        });
    });

    teamButton.addEventListener('mouseleave', function() {
        gsap.to(teamButton, {
            duration: 0.1,
            backgroundColor: "transparent",
            color: "#007bff",
            borderRadius: "0px",
            ease: "power2.out"
        });
    });
});

