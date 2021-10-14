import pandas
import sqlalchemy.orm
import sqlalchemy.sql.schema
from sqlalchemy import select
import datetime
from app.database.tables_declaration import *


def update_tables(data_df: pandas.DataFrame,
                  session_maker: sqlalchemy.orm.session.sessionmaker) -> None:
    """Function that takes all_data DataFrame, splits it, normalizes, creates relation tables and puts everything into Database.
    Same functionality as update_PostgreSQL_procedure.create_PostgreSQL but arguably smoother. Although still not without flaws."""
    session = session_maker()
    for i in data_df.index:
        statement = select(JobOffer).where(JobOffer.offer_url == data_df.loc[i, 'offer_url'])
        if session.execute(statement).fetchone() is None:
            job_offer = JobOffer(title=data_df.loc[i, 'title'],
                                 b2b_min=data_df.loc[i, 'b2b_min'],
                                 b2b_max=data_df.loc[i, 'b2b_max'],
                                 permanent_min=data_df.loc[i, 'permanent_min'],
                                 permanent_max=data_df.loc[i, 'permanent_max'],
                                 mandate_min=data_df.loc[i, 'mandate_min'],
                                 mandate_max=data_df.loc[i, 'mandate_max'],
                                 expired=data_df.loc[i, 'expired'],
                                 scraped_at=data_df.loc[i, 'scraped_at'],
                                 offer_url=data_df.loc[i, 'offer_url']
                                 )
            statement = select(Company).where(Company.name == data_df.loc[i, 'company'])
            is_already = session.execute(statement).fetchone()
            if is_already is None:
                job_offer.to_company = Company(data_df.loc[i, 'company'],
                                               data_df.loc[i, 'company_size'])
            else:
                job_offer.to_company = is_already[0]

            statement = select(Jobsite).where(Jobsite.name == data_df.loc[i, 'jobsite'])
            is_already = session.execute(statement).fetchone()
            if is_already is None:
                job_offer.to_jobsite = Jobsite(data_df.loc[i, 'jobsite'])
            else:
                job_offer.to_jobsite = is_already[0]

            job_offer.to_location = is_already_for_list_like(data_df, i, 'location', session, Location, Location.name)

            job_offer.to_experience = is_already_for_list_like(data_df, i, 'experience', session, Experience,
                                                               Experience.level)

            job_offer.to_employment_type = is_already_for_list_like(data_df, i, 'employment_type', session,
                                                                    EmploymentType, EmploymentType.type)

            job_offer.to_skill_must = is_already_for_list_like(data_df, i, 'skills_must', session,
                                                               Skill, Skill.name)

            job_offer.to_skill_nice = is_already_for_list_like(data_df, i, 'skills_nice', session,
                                                               Skill, Skill.name)

            session.add(job_offer)
    session.commit()
