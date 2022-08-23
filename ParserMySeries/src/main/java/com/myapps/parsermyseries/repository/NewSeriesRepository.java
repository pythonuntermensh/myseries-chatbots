package com.myapps.parsermyseries.repository;

import com.myapps.parsermyseries.entity.NewSeriesEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NewSeriesRepository extends JpaRepository<NewSeriesEntity, Long> {
    NewSeriesEntity findByName(String name);
    List<NewSeriesEntity> findAllByVKDeprecated(Boolean VKDeprecated);
    List<NewSeriesEntity> findAllByTGDeprecated(Boolean TGDeprecated);
    List<NewSeriesEntity> findAllByVKDeprecatedAndTGDeprecated(Boolean VKDeprecated, Boolean TGDeprecated);
}
