const appBarElement = document.getElementsByClassName('topbar')[0];
const wrapperElement = document.getElementsByClassName('content-wrapper')[0];

const appBarHeight = appBarElement.clientHeight;
appBarElement.style.height = appBarHeight + 'px';
let lastContentScrollTop = 0;

function scrollListener(){
  const currentContentScrollTop = wrapperElement.scrollTop;

  currentAppBarHeight = parseInt(appBarElement.style.height);
  console.log(currentAppBarHeight);
  if (currentContentScrollTop > lastContentScrollTop) {
    let newAppBarHeight;
    // user is scrolling down
    if (currentAppBarHeight > bannerHeight) {
      // appbar is not entirely collapsed
      let newAppBarHeight =
        currentAppBarHeight -
        (currentContentScrollTop - lastContentScrollTop);
      // set position limit
      newAppBarHeight =
        newAppBarHeight > bannerHeight
          ? newAppBarHeight
          : bannerHeight;
      appBarElement.style.height = newAppBarHeight + 'px';
      appBarElement.style.opacity = (newAppBarHeight / (appBarHeight - bannerHeight)) * 100 + '%';

    }
  } else {
    // user is scrolling up
    if (currentAppBarHeight < appBarHeight) {
      // appbar is not entirely displayed
      let newAppBarHeight;

      if ((appBarHeight - bannerHeight)  > currentContentScrollTop) {
        newAppBarHeight =
            currentAppBarHeight +
            (lastContentScrollTop - currentContentScrollTop);
        // set position limit
        newAppBarHeight =
            newAppBarHeight > appBarHeight ? appBarHeight : newAppBarHeight;

        appBarElement.style.height = newAppBarHeight + 'px';
        appBarElement.style.opacity = (newAppBarHeight / (appBarHeight - bannerHeight)) * 100 + '%';
      }
    }
  }

  lastContentScrollTop = currentContentScrollTop;
}

wrapperElement.addEventListener('scroll', scrollListener);