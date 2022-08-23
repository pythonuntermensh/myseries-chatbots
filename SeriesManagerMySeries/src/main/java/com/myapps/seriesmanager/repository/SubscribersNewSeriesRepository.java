package com.myapps.seriesmanager.repository;

import com.myapps.seriesmanager.entity.SubscribersNewSeriesEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SubscribersNewSeriesRepository extends JpaRepository<SubscribersNewSeriesEntity, Long> {
}
