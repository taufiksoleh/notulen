package com.notulen.di

import android.content.Context
import androidx.room.Room
import com.notulen.BuildConfig
import com.notulen.data.local.dao.MeetingDao
import com.notulen.data.local.database.NotulenDatabase
import com.notulen.data.remote.api.NotulenApiService
import com.notulen.data.repository.AudioRepositoryImpl
import com.notulen.data.repository.MeetingRepositoryImpl
import com.notulen.domain.repository.AudioRepository
import com.notulen.domain.repository.MeetingRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import timber.log.Timber
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        val loggingInterceptor = HttpLoggingInterceptor { message ->
            Timber.tag("OkHttp").d(message)
        }.apply {
            level = if (BuildConfig.DEBUG) {
                HttpLoggingInterceptor.Level.BODY
            } else {
                HttpLoggingInterceptor.Level.NONE
            }
        }

        return OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideNotulenApiService(retrofit: Retrofit): NotulenApiService {
        return retrofit.create(NotulenApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideNotulenDatabase(@ApplicationContext context: Context): NotulenDatabase {
        return Room.databaseBuilder(
            context,
            NotulenDatabase::class.java,
            NotulenDatabase.DATABASE_NAME
        )
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    @Singleton
    fun provideMeetingDao(database: NotulenDatabase): MeetingDao {
        return database.meetingDao()
    }

    @Provides
    @Singleton
    fun provideMeetingRepository(
        apiService: NotulenApiService,
        meetingDao: MeetingDao
    ): MeetingRepository {
        return MeetingRepositoryImpl(apiService, meetingDao)
    }

    @Provides
    @Singleton
    fun provideAudioRepository(
        @ApplicationContext context: Context
    ): AudioRepository {
        return AudioRepositoryImpl(context)
    }
}
