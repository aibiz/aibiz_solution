const getStackIcon = (icon, transform) => {
  return `
      <span class="fa-stack ml-n1 mr-3">
        <i class="fas fa-circle fa-stack-2x text-200"></i>
        <i class="${icon} fa-stack-1x text-primary" data-fa-transform=${transform}></i>
      </span>
    `;
};

const getTemplate = (info) => {
  return `
  <div class="modal-header px-card bg-light border-0 flex-between-center">
    <div>
      <h5 class="mb-0">${info.event.title}</h5>
      ${
        !!info.event.extendedProps.organizer
          ? `<p class="mb-0 fs--1 mt-1">
          by <a href="#!">${info.event.extendedProps.organizer}</a>
        </p>`
          : ''
      }
    </div>
    
    <button class="close fs-0 px-card" data-dismiss="modal" aria-label="Close">
      <span class="fas fa-times"></span>
    </button>
  </div>
  <div class="modal-body px-card pb-card pt-1 fs--1">
    ${
      info.event.extendedProps.description
        ? `
        <div class="media mt-3">
          ${getStackIcon('fas fa-align-left')}
          <div class="media-body">
            <h6>Description</h6>
            <p class="mb-0">
              
            ${info.event.extendedProps.description
              .split(' ')
              .slice(0, 30)
              .join(' ')}
            </p>
          </div>
        </div>
      `
        : ''
    } 
    <div class="media mt-3">
      ${getStackIcon('fas fa-calendar-check')}
      <div class="media-body">
          <h6>Date and Time</h6>
          <p class="mb-1">
            ${
              window.dayjs &&
              window
                .dayjs(info.event.start)
                .format('dddd, MMMM D, YYYY, h:mm A')
            } 
            ${
              info.event.end
                ? `– <br/>${
                    window.dayjs &&
                    window
                      .dayjs(info.event.end)
                      .subtract(1, 'day')
                      .format('dddd, MMMM D, YYYY, h:mm A')
                  }`
                : ''
            }
          </p>
      </div>
    </div>
    ${
      info.event.extendedProps.location
        ? `
          <div class="media mt-3">
            ${getStackIcon('fas fa-map-marker-alt')}
            <div class="media-body">
                <h6>Location</h6>
                <div class="mb-1">${info.event.extendedProps.location}</div>
            </div>
          </div>
        `
        : ''
    }
    ${
      info.event.extendedProps.schedules
        ? `
          <div class="media mt-3">
          ${getStackIcon('fas fa-clock')}
          <div class="media-body">
              <h6>Schedule</h6>
              
              <ul class="list-unstyled timeline mb-0">
                ${info.event.extendedProps.schedules
                  .map((schedule) => `<li>${schedule.title}</li>`)
                  .join('')}
              </ul>
          </div>
        `
        : ''
    }
    </div>
  </div>
  <div class="modal-footer d-flex justify-content-end bg-light px-card border-top-0">
    <a href="pages/event-create.html" class="btn btn-falcon-default btn-sm">
      <span class="fas fa-pencil-alt fs--2 mr-2"></span> Edit
    </a>
    <a href='pages/event-detail.html' class="btn btn-falcon-primary btn-sm">
      See more details
      <span class="fas fa-angle-right fs--2 ml-1"></span>
    </a>
  </div
  `;
};

export default getTemplate;
