FROM python:3.10.4 as base

ENV PATH /home/user/.local/bin:$PATH
RUN useradd -m user
WORKDIR /app
USER user

COPY ./requirements requirements
RUN pip install --upgrade --user pip \
    && pip install --user --no-cache-dir -r requirements/base.txt

COPY --chown=user . /app

FROM base as prod

USER user

COPY --chown=user --from=base /home .
COPY --chown=user --from=base /app .

WORKDIR /app

CMD ["python", "./wsgi_app.py"]


FROM prod as tests
WORKDIR /app

USER user

COPY --chown=user --from=prod /home .
RUN pip install --user --no-cache-dir -r requirements/dev.txt

COPY --chown=user --from=prod /app .
COPY --chown=user tests .

CMD ["make", "test"]