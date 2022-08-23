package com.myapps.parsermyseries.repository;

import com.myapps.parsermyseries.entity.NoveltySeriesEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NoveltySeriesRepository extends JpaRepository<NoveltySeriesEntity, Long> {
    NoveltySeriesEntity findByName(String name);
    List<NoveltySeriesEntity> findAllByVKDeprecated(boolean vk);
    List<NoveltySeriesEntity> findAllByTGDeprecated(boolean vk);
}
