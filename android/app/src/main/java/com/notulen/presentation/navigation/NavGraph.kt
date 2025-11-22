package com.notulen.presentation.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.notulen.presentation.ui.MeetingDetailScreen
import com.notulen.presentation.ui.MeetingsScreen
import com.notulen.presentation.ui.RecordScreen

@Composable
fun NavGraph(
    navController: NavHostController,
    startDestination: String = Screen.Meetings.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(route = Screen.Meetings.route) {
            MeetingsScreen(
                onNavigateToRecord = {
                    navController.navigate(Screen.Record.route)
                },
                onNavigateToDetail = { meetingId ->
                    navController.navigate(Screen.MeetingDetail.createRoute(meetingId))
                }
            )
        }

        composable(route = Screen.Record.route) {
            RecordScreen(
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        composable(
            route = Screen.MeetingDetail.route,
            arguments = listOf(
                navArgument("meetingId") {
                    type = NavType.StringType
                }
            )
        ) { backStackEntry ->
            val meetingId = backStackEntry.arguments?.getString("meetingId") ?: return@composable
            MeetingDetailScreen(
                meetingId = meetingId,
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}

sealed class Screen(val route: String) {
    object Meetings : Screen("meetings")
    object Record : Screen("record")
    object MeetingDetail : Screen("meeting_detail/{meetingId}") {
        fun createRoute(meetingId: String) = "meeting_detail/$meetingId"
    }
}
